#!/bin/bash  bash script/llm_gen_api.sh
model=$1
api_base=$2
api_key=$3
questions_file=$4
version=$5
language_type=$6
output_dir="output/answer/$version"
max_tokens=4096
parallel=50

echo "[llm_gen_api] model: $model"

python src/llm_gen/gen_api_answer.py \
    --model $model \
    --api_base $api_base \
    --api_key $api_key \
    --questions_file $questions_file \
    --output_dir $output_dir \
    --max_tokens $max_tokens \
    --parallel $parallel \
    --language_type $language_type