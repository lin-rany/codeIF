#!/bin/bash bash script/llm_judge.sh
gen_model=$1
version=$2
language_type=$3

api_base=""
api_key=""
judge_model=""

answer_file="output/answer/$version/$gen_model.jsonl"
output_dir="output/judge/$version"
max_tokens=4096
parallel=50
python src/llm_gen/gen_judge.py \
    --api_base $api_base \
    --api_key $api_key \
    --gen_model $gen_model \
    --judge_model $judge_model\
    --answer_file $answer_file \
    --output_dir $output_dir \
    --max_tokens $max_tokens \
    --parallel $parallel \
    --language_type $language_type