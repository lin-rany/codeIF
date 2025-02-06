#!/bin/bash bash script/llm_gen_local.sh
model_id=$1

model_path=model/$model_id
questions_file="data/question/zh.json"
output_dir="output/answer"
max_new_tokens=2048
language_type="zh"
parallel=5

python src/llm_gen/gen_model_ans.py \
    --model_path $model_path \
    --model_id $model_id \
    --questions_file $questions_file \
    --output_dir $output_dir \
    --max_new_tokens $max_new_tokens \
    --temperature 0.5 \
    --device cuda \
    --parallel $parallel