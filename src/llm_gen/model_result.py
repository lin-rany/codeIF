import argparse
import ast
from utils import file_util
import pandas as pd
import os
import re

def extract_list(string):
    start = string.find('[')
    end = string.find(']', start)
    list_str = string[start:end+1]
    # If the list elements are not in quotes, add them
    if not re.search(r'"', list_str) and not re.search(r"'", list_str):
        list_str = re.sub(r'([a-zA-Z]+)', r'"\1"', list_str)
    
     # Try to parse the string into a list
    try:
        result_list = ast.literal_eval(list_str)
    except SyntaxError:
        print(f"无法从字符串中提取列表：{string}")
        result_list = ['No']
    if len(result_list) == 0:
        print(f"Unable to extract list from string: {string}")
    return result_list
def calculate_count(list):
    yes_count = list.count('Yes')
    return yes_count
def calculate_full_dependence_count(list,dependence_map):
    count=0
    for idx,item in enumerate(list):
        if item!='Yes':
            continue
        if str(idx) not in dependence_map:
            count=count+1
        else:
            all_right=True
            for dependence_idx in dependence_map[str(idx)]:
                if list[dependence_idx]!='Yes':
                    all_right=False
                    break
            count=count+(all_right==True)
    return count
def calculate_full_check_list_count(check_list):
    max_yes = 0
    current_yes = 0
    for item in check_list:
        if item == 'Yes':
            current_yes += 1
            max_yes = max(max_yes, current_yes)
        else:
            current_yes = 0
    return max_yes
def calculate_model_result(gen_model,judge_model,version='dafault'):
    # print(f"gen_model:{gen_model},judge_model:{judge_model}")
    judge_file="output/judge/"+version+'/'+judge_model+"-"+gen_model+".jsonl"
    judge_results=file_util.read_jsonl(judge_file)
    score_list=[]
    dependence_score_list=[]
    checklist_score_list=[]
    
    for judge_result in judge_results:
        result_list=extract_list(judge_result['judge_result'])
        if len(result_list)!=len(judge_result['instruction_list']):
            print(f"judge len not match judge_result {judge_result['judge_result']}: instruction_list:{judge_result['instruction_list']}")
            continue
        score_list.append(calculate_count(result_list)/len(result_list))
        dependence_score_list.append(calculate_full_dependence_count(result_list,judge_result['instruction_dependence'])/len(result_list))
        checklist_score_list.append(calculate_full_check_list_count(result_list)/len(result_list))
    score_result={
        'full_result':sum([1 for score in score_list if score==1])/len(score_list),
        'mean':sum(score_list)/len(score_list),
        'dependence_score_mean':sum(dependence_score_list)/len(score_list),
        'check_list_socre_mean':sum(checklist_score_list)/len(score_list),
        'score_list':len(score_list),
        'gen_model':gen_model,
        'judge_model': judge_model,
    }
    return score_result

def main():
    
    parser = argparse.ArgumentParser(description="Generate answers using a local model.")
    # 添加生成模型路径或Hugging Face模型ID的参数
    parser.add_argument(
        "--gen_model_list", 
        type=str, 
        required=True, 
        help="Path to the generation model or Hugging Face model ID."
    )

    # 添加用于判断的模型路径或Hugging Face模型ID的参数
    parser.add_argument(
        "--judge_model", 
        type=str, 
        required=True, 
        help="Path to the judge model or Hugging Face model ID."
    )

    parser.add_argument(
        "--version", 
        type=str, 
        default="default",
        required=True, 
        help="version"
    )
    # 添加输出目录的参数
    parser.add_argument(
        "--output_dir", 
        type=str, 
        required=True, 
        help="Directory where the output will be saved."
    )
    args=parser.parse_args()
    print(args)
    
    model_result_list=[calculate_model_result(gen_model,args.judge_model,args.version) for gen_model in args.gen_model_list.split(',')]
    for model_result in model_result_list:
        print(model_result)
    # 将数据转换为pandas DataFrame
    df = pd.DataFrame(model_result_list)
    output_file=os.path.join(args.output_dir, f"model_result.csv")
    # 将DataFrame保存为.csv文件
    file_util.try_write(output_file)
    df.to_csv(output_file, index=False)
    
if __name__=='__main__':
    main()



    





# %%






