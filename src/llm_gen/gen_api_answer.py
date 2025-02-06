import argparse
from utils import question_util,file_util
from utils import api_util
import tqdm
import concurrent.futures
import os
import shortuuid
import time
import json
def get_answer(
    question,
    model,
    max_tokens,
    answer_file,
    temperature=0.5,
    api_dict=None,
):
    output=api_util.API_ERROR_OUTPUT
    prompt = question["prompt"]
    if model in question_util.DEEPSEEK_MODEL_LIST:
        output = api_util.chat_completion_deepseek(model,prompt, temperature, max_tokens, api_dict=api_dict)
    elif api_dict is not None:
        output = api_util.chat_completion_openai(model,prompt, temperature, max_tokens, api_dict=api_dict)
    ans_json = {
            "question_id": question["question_id"],
            "model_id": model,
            "answer_id": shortuuid.uuid(),
            "tstamp": time.time(),
            "question": question["question"],
            "instruction_list":question["instruction_list"],
            "instruction_dependence":question["instruction_dependence"],
            "prompt": prompt,
            "answer": output,
            "meta_info":question["meta_info"],
        }  
    file_util.write_data_to_file(answer_file,[ans_json],'a')  
    return output

def run_questions(parallel, questions, model, max_tokens, answer_dir, api_dict):
    answer_file = os.path.join(answer_dir, f"{model}.jsonl") 
    if parallel == 1:
        for question in tqdm.tqdm(questions):
            get_answer(
                question,
                model,
                max_tokens,
                answer_file,
                api_dict=api_dict,
            )
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = []
            for question in questions:
                future = executor.submit(
                    get_answer,
                    question,
                    model,
                    max_tokens,
                    answer_file,
                    api_dict=api_dict,
                )
                futures.append(future)      
            progress = tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures))
            for future in progress:
                progress.set_description(f"Processing with model: {model}")
                future.result()
    if len(questions) > 0:
        question_util.reorg_answer_file(answer_file)


def main():
    parser = argparse.ArgumentParser(description="Generate answers using a api server.")
    parser.add_argument(
        "--api_base",
        type=str,
        default=None,
        help="If provided, will be used as the base of an openai API request",
    )
    parser.add_argument(
        "--api_key",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
    )
    parser.add_argument("--model", type=str, default="deepseek-chat", help="Model to use.")
    parser.add_argument(
        "--force_temperature", type=float,default=0.5, help="Forcibly set a sampling temperature."
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=4096,
        help="The maximum number of new generated tokens.",
    )
    parser.add_argument(
        "--parallel", type=int, default=1, help="The number of concurrent API calls."
    )
    parser.add_argument(
        "--questions_file", type=str, required=True, help="Path to the JSONL file containing questions."
    )
    parser.add_argument(
        "--language_type", type=str,  default='zh', choices=['zh', 'en'], help="Language type for the questions."
    )
    args = parser.parse_args()
    print(args)
    # 加载问题
    questions=question_util.load_questions_v3(args.questions_file,args.language_type)
    print(f"Loaded {len(questions)} questions.")
    run_questions(
        args.parallel,
        questions,
        args.model,
        args.max_tokens,
        args.output_dir,
        {
            "api_base": args.api_base,
            "api_key": args.api_key,
        }
    )
if __name__ == "__main__":
    main()
        