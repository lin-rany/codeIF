import argparse
import json
import os
import time
import torch
from tqdm import tqdm
import shortuuid
import utils.file_util as file_util  # 导入模块
import utils.question_util as question_util  # 导入模块
import concurrent.futures

from fastchat.model import load_model,get_conversation_template

# 工具方法：加载模型和 tokenizer
def load_model_and_tokenizer(model_path, dtype=None, revision='main', device='cuda', num_gpus=1, max_gpu_memory=None):
    """
    加载模型和 tokenizer。

    Args:
        model_path (str): 模型路径或 Hugging Face 模型 ID。
        dtype (str): 模型数据类型（如 "float32", "float16", "bfloat16"）。
        revision (str): 模型版本。
        device (str): 设备类型（如 "cuda" 或 "cpu"）。
        num_gpus (int): 使用的 GPU 数量。
        max_gpu_memory (str): 每个 GPU 的最大内存限制。

    Returns:
        model, tokenizer: 加载的模型和 tokenizer。
    """
    
    model, tokenizer = load_model(
        model_path,
        revision=revision,
        device=device,
        num_gpus=num_gpus,
        max_gpu_memory=max_gpu_memory,
        dtype=dtype,
        load_8bit=False,
        cpu_offloading=False,
        debug=False,
    )
    model.generation_config.pad_token_id = tokenizer.pad_token_id
    return model, tokenizer

# 工具方法：生成单个答案
@torch.inference_mode()
def generate_answer(model, tokenizer, conv_template, max_new_tokens=4096, temperature=0.5, stop_str=None):
    """
    根据给定的 prompt 生成答案。

    Args:
        model: 加载的模型。
        tokenizer: 加载的 tokenizer。
        conv_template (conv_template): 输入的 prompt。
        max_new_tokens (int): 生成的最大 token 数量。
        temperature (float): 生成温度。
        stop_str (str or list): 停止字符串（可以是单个字符串或字符串列表）。

    Returns:
        str: 生成的答案。
    """
    prompt=conv_template.get_prompt()
    # input_ids = tokenizer([prompt]).input_ids
    inputs = tokenizer(prompt, return_tensors="pt")
    do_sample = True
    try:
        from transformers.generation.streamers import TextStreamer
        output_ids = model.generate(
            # torch.as_tensor(input_ids).cuda(),
            inputs['input_ids'].cuda(),
            attention_mask=inputs['attention_mask'].cuda(),
            do_sample=do_sample,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            # streamer=TextStreamer(tokenizer)
        )
        if model.config.is_encoder_decoder:
            output_ids = output_ids[0]
        else:
            output_ids = output_ids[0][len(inputs['input_ids'][0]) :]

        # be consistent with the template's stop_token_ids
        if conv_template.stop_token_ids:
            stop_token_ids_index = [
                i
                for i, id in enumerate(output_ids)
                if id in conv_template.stop_token_ids
            ]
            if len(stop_token_ids_index) > 0:
                output_ids = output_ids[: stop_token_ids_index[0]]

        output = tokenizer.decode(
            output_ids,
            spaces_between_special_tokens=False,
        )
        if conv_template.stop_str and isinstance(conv_template.stop_str, list):
            stop_str_indices = sorted(
                [
                    output.find(stop_str)
                    for stop_str in conv_template.stop_str
                    if output.find(stop_str) > 0
                ]
            )
            if len(stop_str_indices) > 0:
                output = output[: stop_str_indices[0]]
        elif conv_template.stop_str and output.find(conv_template.stop_str) > 0:
            output = output[: output.find(conv_template.stop_str)]

        for special_token in tokenizer.special_tokens_map.values():
            if isinstance(special_token, list):
                for special_tok in special_token:
                    output = output.replace(special_tok, "")
            else:
                output = output.replace(special_token, "")
        output = output.strip()

        if conv_template.name == "xgen" and output.startswith("Assistant:"):
            output = output.replace("Assistant:", "", 1).strip()

        # # 处理停止字符串
        # output = tokenizer.decode(output_ids, spaces_between_special_tokens=False,skip_special_tokens=True)
        # if stop_str:
        #     if isinstance(stop_str, list):
        #         stop_indices = sorted([output.find(s) for s in stop_str if output.find(s) > 0])
        #         if stop_indices:
        #             output = output[:stop_indices[0]]
        #     elif output.find(stop_str) > 0:
        #         output = output[:output.find(stop_str)]

        # # 去除特殊字符
        # for special_token in tokenizer.special_tokens_map.values():
        #     if isinstance(special_token, list):
        #         for tok in special_token:
        #             output = output.replace(tok, "")
        #     else:
        #         output = output.replace(special_token, "")
        # output = output.strip()

    except RuntimeError as e:
        print(f"Error generating answer: {e}")
        output = "ERROR"

    return output
def load_conversation_template(model_path):
    """
    加载对话模板。
    Args:
        model_path (str): 模型路径或 Hugging Face 模型 ID。
    Returns:
        conversation: 对话模板。
    """
    
    conversation = get_conversation_template(model_path)
    return conversation

def generate_answer_and_write(conv_template,model_id,model, tokenizer, question,answer_file, max_new_tokens=4096, temperature=0.5, stop_str=None):
    question_prompt = question["prompt"]
    conv_template.append_message(conv_template.roles[0], question_prompt)
    conv_template.append_message(conv_template.roles[1], None)
    prompt = conv_template.get_prompt()
    answer = generate_answer(model, tokenizer, conv_template, max_new_tokens, temperature, stop_str)
    ans_json = {
        "question_id": question["question_id"],
        "model_id": model_id,
        "answer_id": shortuuid.uuid(),
        "tstamp": time.time(),
        "question": question["question"],
        "instruction_list":question["instruction_list"],
        "prompt": prompt,
        "answer": answer,
    }
    file_util.write_data_to_file(answer_file,[ans_json],'a')      

# 工具方法：批量生成答案
def batch_generate_answers(parallel,conv_template,model, tokenizer, questions, output_dir, model_id, max_new_tokens=4096, temperature=0.0, stop_str=None):
    """
    批量生成答案并将结果保存到文件中。

    Args:
        model: 加载的模型。
        tokenizer: 加载的 tokenizer。
        questions (list): 问题列表，每个问题是一个字典，包含 "question_id" 和 "prompt"。
        output_dir (str): 输出目录。
        model_id (str): 模型 ID。
        max_new_tokens (int): 生成的最大 token 数量。
        temperature (float): 生成温度。
        stop_str (str or list): 停止字符串。
    """
    os.makedirs(output_dir, exist_ok=True)
    answer_file = os.path.join(output_dir, f"{model_id}.jsonl")
    if parallel==1:
        for question in tqdm(questions):
            generate_answer_and_write(
                conv_template=conv_template,
                model_id=model_id,
                model=model,
                tokenizer=tokenizer,
                question=question,
                answer_file=answer_file,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                stop_str=stop_str,
            )
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
            print(timer.post(f"parallel {parallel} executor"))
            futures = []
            for question in questions:
                future = executor.submit(
                    generate_answer_and_write,
                    conv_template=conv_template,
                    model_id=model_id,
                    model=model,
                    tokenizer=tokenizer,
                    question=question,
                    answer_file=answer_file,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    stop_str=stop_str,
                )  
                futures.append(future)   
            print(timer.post("summit all task"))
            for future in tqdm(
                concurrent.futures.as_completed(futures),
                total=len(futures),
                mininterval=0.5
            ):
                future.result()
                
    if len(questions) > 0:
        question_util.reorg_answer_file(answer_file)
    
timer=question_util.TimeLogger()
# 主函数
def main():
    parser = argparse.ArgumentParser(description="Generate answers using a local model.")
    parser.add_argument(
        "--model_path", 
        type=str, 
        required=True, 
        help="Path to the model or Hugging Face model ID."
    )
    parser.add_argument(
        "--model_id", 
        type=str, 
        required=True, 
        help="Custom name for the model."
    )
    parser.add_argument(
        "--questions_file", 
        type=str, 
        required=True, 
        help="Path to the JSONL file containing questions."
    )
    parser.add_argument(
        "--language_type", 
        type=str, 
        default='zh', 
        choices=['zh', 'en'], 
        help="Language type for the questions."
    )
    parser.add_argument(
        "--output_dir", 
        type=str, 
        required=True, 
        help="Directory to save the generated answers."
    )
    parser.add_argument(
        "--max_new_tokens", 
        type=int, 
        default=4096, 
        help="Maximum number of tokens to generate."
    )
    parser.add_argument(
        "--temperature", 
        type=float, 
        default=0.0, 
        help="Sampling temperature for generation."
    )
    parser.add_argument(
        "--stop_str", 
        type=str, 
        default=None, 
        help="Stop string for generation (optional)."
    )
    parser.add_argument(
        "--dtype", 
        type=str, 
        default="float16", 
        choices=["float32", "float16", "bfloat16"], 
        help="Model data type."
    )
    parser.add_argument(
        "--revision", 
        type=str, 
        default="main", 
        help="Model revision to load."
    )
    parser.add_argument(
        "--num_gpus", 
        type=int,
        default=1,
        help="Number of GPUs to use."
    )
    parser.add_argument(
        "--max_gpu_memory",
        type=str, 
        default=None, 
        help="Maximum GPU memory per GPU."
    )
    parser.add_argument(
        "--device", 
        type=str, 
        default="cuda", 
        help="Device to use (e.g., 'cuda' or 'cpu')."
    )
    parser.add_argument(
        "--parallel", 
        type=int, 
        default=1, 
        help="parallel num"
    )
    
    args = parser.parse_args()
    print(args)
     # 加载问题
    questions=question_util.load_questions(args.questions_file,args.language_type)
    print(timer.post(f"finish load question len:{len(questions)}"))
   
    model, tokenizer = load_model_and_tokenizer(
        args.model_path,
        dtype=args.dtype,
        revision=args.revision,
        device=args.device,
        num_gpus=args.num_gpus,
        max_gpu_memory=args.max_gpu_memory,
    )
    print(timer.post("load model finish"))
    
    conv_template=get_conversation_template(args.model_path)
    print(timer.post(f"load conv_template finish conv_template:{conv_template}"))
    # 批量生成答案
    batch_generate_answers(
        parallel=args.parallel,
        conv_template=conv_template,
        model=model,
        tokenizer=tokenizer,
        questions=questions,
        output_dir=args.output_dir,
        model_id=args.model_id,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        stop_str=args.stop_str,
    )

# 运行主函数
if __name__ == "__main__":
    main()