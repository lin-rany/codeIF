#!/bin/bash bash script/model_result.sh

version=$1
gen_model_list=$2

echo "[model_result] version: $version"
echo "[model_result] gen_model_list: $gen_model_list"

judge_model="gpt-4o-2024-11-20"
output_dir="output/model_result/$version"

python src/llm_gen/model_result.py \
    --gen_model_list $gen_model_list \
    --judge_model $judge_model \
    --output_dir $output_dir \
    --version $version