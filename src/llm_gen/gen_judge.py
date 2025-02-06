import argparse
from utils import question_util,file_util,instruction_util
import prompts.CODEIF_judge 
from utils import api_util
import tqdm
import concurrent.futures
import os
import shortuuid
import time
import json

def get_judge(judge_question,judge_model,max_tokens,output_file,api_dict,temperature=0.5,language_type='zh'):
    output=api_util.API_ERROR_OUTPUT
    prompt=prompts.CODEIF_judge.ZH_JUDGE_PROMPT
    if language_type=='en':
        prompt=prompts.CODEIF_judge.EN_JUDGE_PROMPT
    instructions_str=question_util.build_instructions_str(judge_question["instruction_list"])
    judge_prompt=prompt.format(
        question=judge_question["question"],
        instructions_str=instructions_str,
        generated_code=judge_question["answer"])
    if judge_model in question_util.DEEPSEEK_MODEL_LIST:
        output = api_util.chat_completion_deepseek(judge_model,judge_prompt, temperature, max_tokens, api_dict=api_dict)
    elif api_dict is not None:
        output = api_util.chat_completion_openai(judge_model,judge_prompt, temperature, max_tokens, api_dict=api_dict)
    
    # output = api_util.chat_completion_deepseek(judge_model,judge_prompt, temperature, max_tokens, api_dict=api_dict)
    # judge_ans=judge_question
    judge_question['judge_result']=output 
    judge_question['judge_prompt']=judge_prompt
    file_util.write_data_to_file(output_file,[judge_question],'a')  
    return output

def run_judges(parallel, questions, gen_model,judge_model, max_tokens, output_dir, api_dict,language_type='zh'):
    output_file = os.path.join(output_dir, f"{judge_model}-{gen_model}.jsonl") 
    if parallel == 1:
        for question in tqdm.tqdm(questions):
            get_judge(
                judge_question=question,
                judge_model=judge_model,
                max_tokens=max_tokens,
                output_file=output_file,
                api_dict=api_dict, 
                language_type=language_type,
            )
        if len(questions) > 0:
            question_util.reorg_answer_file(output_file)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = []
            for question in questions:
                future = executor.submit(
                    get_judge,
                    question,
                    judge_model,
                    max_tokens,
                    output_file,
                    api_dict=api_dict,
                    language_type=language_type,
                )
                futures.append(future)      

            for future in tqdm.tqdm(
                concurrent.futures.as_completed(futures), total=len(futures)
            ):
                future.result()
        if len(questions) > 0:
            question_util.reorg_answer_file(output_file)

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
    parser.add_argument(
        "--judge_model", type=str,
        default="deepseek-chat",
        help="Model to judge."
    )
    parser.add_argument(
        "--gen_model", type=str,
        default="",
        help="Model to gen."
    )
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
        "--answer_file", type=str, required=True, help="Path to the JSONL file containing answer."
    )
    parser.add_argument(
        "--language_type", type=str,  default='zh', choices=['zh', 'en'], help="Language type for the questions."
    )
    args = parser.parse_args()
    print(args)
    # 加载模型问题
    judge_questions=file_util.read_jsonl(args.answer_file)
    print(f"Loaded {len(judge_questions)} judge_questions.")
    run_judges(
        parallel=args.parallel,
        questions=judge_questions,
        judge_model=args.judge_model,
        gen_model=args.gen_model,
        max_tokens=args.max_tokens,
        output_dir=args.output_dir,
        api_dict={
            "api_base": args.api_base,
            "api_key": args.api_key,
        },
        language_type=args.language_type
    )
if __name__ == "__main__":
    main()