import errno
import os
import csv
import json
from functools import wraps
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

import functools
def save_to_csv(data_row_list, filename="output.csv"):
    # 确定CSV文件的标题行，根据字典的键
    headers = data_row_list[0].keys()
    
    # 打开CSV文件，准备写入
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # 写入标题行
        writer.writeheader()
        # 逐行写入数据
        for row in data_row_list:
            writer.writerow(row)

def try_write(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
def write_data_to_file(filepath, dataList,write_mode='w'):
    """写入JSON数据到给定文件路径中
    参数：
        filepath (str): 文件路径
        dataList (lust): 包含新数据的list
        write_mode (str): 写入模式
    返回:
        无
    """
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, write_mode,encoding='utf-8') as fout:
        for data in dataList:
            fout.write(json.dumps(data,ensure_ascii=False) + "\n")

def write_json_to_file(filepath, data):
    """写入JSON数据到给定文件路径中,并覆盖原文件。

    参数：
        filepath (str): 文件路径
        data (dict): 包含新数据的字典

    返回:
        无
    """
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file)

def read_json_from_file(filepath):
    read_ok=False
    results={}
    if os.path.exists(filepath):
        read_ok=True
        # print(f"load beir result from file:{result_file}")
        with open(filepath, 'r') as f:
            results = json.load(f)
    return read_ok,results


def read_jsonl(filepath):
    """
    读取jsonl文件
    """
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        return [json.loads(l) for l in f.readlines()]
