from . import file_util
from . import instruction_util
from prompts.CODEIF_instruction import *
import os
import json
import time
def load_questions(questions_file,language_type='zh'):
    """
    从 JSONL 文件加载问题。
    Args:
        questions_file (str): 问题文件的路径。
        language_type (str): 语言类型 ('zh' 或 'en')
    Returns:
        list: 问题列表，每个问题是一个字典。
    """
    
    instruction_build_util=instruction_util.instruction_build_util()
    question_list=[]
    _, file_ext = os.path.splitext(questions_file)
    if file_ext=='.json':
        _,question_list=file_util.read_json_from_file(questions_file)
    if file_ext=='.jsonl':
        question_list=file_util.read_jsonl(questions_file)
    for question in question_list:
        instruction_str_list= []
        for instruction in question['instruction_list']: 
            instruction_str_list.append(instruction_build_util.build_instruction(instruction['instruction_id'],instruction['instruction_variable']))
        question['prompt']=build_question_prompt(question['question'],instruction_str_list,language_type)
        question['instruction_list']=instruction_str_list
        question['instruction_str']=build_instructions_str(instruction_str_list)
    return question_list


def load_questions_v2(questions_file,language_type='zh'):
    """
    从 JSONL 文件加载问题。
    Args:
        questions_file (str): 问题文件的路径。
        language_type (str): 语言类型 ('zh' 或 'en')
    Returns:
        list: 问题列表，每个问题是一个字典。
    """
    question_list=[]
    _, file_ext = os.path.splitext(questions_file)
    if file_ext=='.json':
        _,question_list=file_util.read_json_from_file(questions_file)
    if file_ext=='.jsonl':
        question_list=file_util.read_jsonl(questions_file)
        
    for question in question_list:
        instruction_str_list=question['instruction_gen_json'][language_type]
        question['question']=question[language_type+'_question']
        question['prompt']=build_question_prompt(question[language_type+'_question'],instruction_str_list,language_type)
        question['instruction_list']=instruction_str_list
        question['instruction_str']=build_instructions_str(instruction_str_list)
    return question_list

def load_questions_v3(questions_file,language_type='zh'):
    """
    从 JSONL 文件加载问题。
    Args:
        questions_file (str): 问题文件的路径。
        language_type (str): 语言类型 ('zh' 或 'en')
    Returns:
        list: 问题列表，每个问题是一个字典。
    """
    question_list=[]
    _, file_ext = os.path.splitext(questions_file)
    if file_ext=='.json':
        _,question_list=file_util.read_json_from_file(questions_file)
    if file_ext=='.jsonl':
        question_list=file_util.read_jsonl(questions_file)
        
    for question in question_list:
        question['prompt']=build_question_prompt(question['question'],question['instruction_list'],language_type)
        question['instruction_str']=build_instructions_str(question['instruction_list'])
    return question_list

def build_question_prompt(question,instruction_list, language_type='zh'):
    """构建问题的提示。
    参数：
        question (str): 问题文本。
        instruction_list (list): 指令列表。
        language_type (str): 语言类型 ('zh' 或 'en')
    返回:
        无
    """
    prompt = EN_PROMPT_TEMPLATE
    if language_type == 'zh':
        prompt = ZH_PROMPT_TEMPLATE
    instructions_str = build_instructions_str(instruction_list)
    return prompt.format(question=question, instructions_str=instructions_str)

def build_instructions_str(instruction_list):
    instruction_list=[instruction['instruction'] for instruction in instruction_list]
    instructions_str = "\n".join([f"{i+1}. {instr}" for i, instr in enumerate(instruction_list)])
    return instructions_str
    

def reorg_answer_file(answer_file):
    """Sort by question id and de-duplication"""
    answers = {}
    with open(answer_file, "r") as fin:
        for l in fin:
            qid = json.loads(l)["question_id"]
            answers[qid] = l

    qids = sorted(list(answers.keys()))
    with open(answer_file, "w") as fout:
        for qid in qids:
            fout.write(answers[qid])

class TimeLogger:
    def __init__(self):
        self.start_time = time.time()
        
    def __call__(self):
        # 重置
        self.start_time = time.time()
        
    def post(self, message):
        end_time = time.time()
        elapsed_time = (end_time - self.start_time) * 1000  # 计算经过的时间，转换为毫秒
        pid = os.getpid()  # 获取当前的PID
        return f"[PID {pid}] already run {elapsed_time:.2f} ms ({message})\n"


ANTHROPIC_MODEL_LIST = (
    "claude-1",
    "claude-2",
    "claude-2.0",
    "claude-2.1",
    "claude-instant-1",
    "claude-instant-1.2",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-20240620",
)

OPENAI_MODEL_LIST = (
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
    "gpt-4-turbo",
    "gpt-4-turbo-2024-04-09",
    "gpt-4-1106-preview",
    "gpt-4-0125-preview",
    "gpt-4o-2024-05-13",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-2024-08-06",
    "chatgpt-4o-latest",
)

INFERENCE_OPENAI_MODEL_LIST = (
    "o1-mini-2024-09-12",
    "o1-mini",
    "o1-preview",
    "o1-preview-2024-09-12",
)

TOGETHER_MODEL_LIST = (
    "Meta-Llama-3.1-405B-Instruct-Turbo",
    "Meta-Llama-3.1-70B-Instruct-Turbo",
    "Meta-Llama-3.1-8B-Instruct-Turbo",
)

GOOGLE_GENERATIVEAI_MODEL_LIST = (
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-001",
    "gemini-1.5-flash-001",
    "gemini-1.5-pro-exp-0801",
    "gemini-1.5-pro-exp-0827",
    "gemini-1.5-flash-exp-0827",
    "gemini-1.5-flash-8b-exp-0827",
    "gemini-1.5-pro-002", 
    "gemini-1.5-flash-002",
)

VERTEX_MODEL_LIST = (
    "gemini-1.5-pro-preview-0409",
)

MISTRAL_MODEL_LIST = (
    "mistral-large-latest",
    "mistral-large-2402",
    "mistral-large",
    "mistral-medium-23-12",
    "mistral-medium",
    "mistral-small-2402",
    "mistral-small",
    "open-mixtral-8x7b",
    "open-mixtral-8x22b",
    "mistral-large-2407",
    "open-mistral-nemo",
)

COHERE_MODEL_LIST = (
    "command-r-plus",
    "command-r",
    "command",
    "command-r-08-2024",
    "command-r-plus-08-2024",
)

DEEPSEEK_MODEL_LIST = (
    "deepseek-coder",
    "deepseek-chat",
)

NVIDIA_MODEL_LIST = (
    "nemotron-4-340b-instruct",
    "llama-3.1-nemotron-70b-instruct",
)

OPENROUTER_MODEL_LIST = (
    "grok-2",
    "grok-2-mini",
)