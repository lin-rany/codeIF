#  bash script/test.sh
xiaohumini_api_base="https://xiaohumini.site/v1"
xiaohumini_api_key=""

aliyuncs_api_base='https://dashscope.aliyuncs.com/compatible-mode/v1'
aliyuncs_api_key=''


deepseek_chat_api_base="https://api.deepseek.com"
deepseek_chat_api_key=""

open_router_api_base="https://openrouter.ai/api/v1"
open_router_api_key=""



declare -A qwen2_5_14b_instruct=( ["model_name"]="qwen2.5-14b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )
declare -A qwen2_5_3b_instruct=( ["model_name"]="qwen2.5-3b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )


declare -A gpt_4o_2024_11_20=( ["model_name"]="gpt-4o-2024-11-20" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )
declare -A gemini_exp_1206=( ["model_name"]="gemini-exp-1206" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )
declare -A llama_3_1_70b_instruct=( ["model_name"]="meta-llama/llama-3.1-70b-instruct" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A llama_3_1_8b_instruct=( ["model_name"]="meta-llama/llama-3.1-8b-instruct" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A ministral_3b=( ["model_name"]="mistralai/ministral-3b" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A phi_3_5_mini_128k_instruct=( ["model_name"]="microsoft/phi-3.5-mini-128k-instruct" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A gemma_2_9b_it=( ["model_name"]="google/gemma-2-9b-it" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A codestral_2501=( ["model_name"]="mistralai/codestral-2501" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A llama_3_3_70b_instruct=( ["model_name"]="meta-llama/llama-3.3-70b-instruct" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A phi_4=( ["model_name"]="microsoft/phi-4" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A gemma_2_27b_it=( ["model_name"]="google/gemma-2-27b-it" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A ministral_8b=( ["model_name"]="mistralai/ministral-8b" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )


declare -A llama3_2_3b_instruct=( ["model_name"]="meta-llama/llama-3.2-3b-instruct" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )
declare -A llama3_2_1b_instruct=( ["model_name"]="meta-llama/llama-3.2-1b-instruct" ["api_base"]=$open_router_api_base ["api_key"]=$open_router_api_key )


declare -A deepseek_chat=( ["model_name"]="deepseek-chat" ["api_base"]=$deepseek_chat_api_base ["api_key"]=$deepseek_chat_api_key )
declare -A deepseek_coder=( ["model_name"]="deepseek-coder" ["api_base"]=$deepseek_chat_api_base ["api_key"]=$deepseek_chat_api_key )


# declare -A chatglm3_6b=( ["model_name"]="chatglm3-6b" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )

declare -A qwen_coder_1_5b_instruct=( ["model_name"]="qwen2.5-coder-1.5b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )
declare -A qwen_coder_3b_instruct=( ["model_name"]="qwen2.5-coder-3b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )
declare -A qwen_coder_7b_instruct=( ["model_name"]="qwen2.5-coder-7b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )
declare -A qwen_coder_14b_instruct=( ["model_name"]="qwen2.5-coder-14b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )

declare -A qwen2_5_1_5b_instruct=( ["model_name"]="qwen2.5-1.5b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )
declare -A qwen2_5_7b_instruct=( ["model_name"]="qwen2.5-7b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )
declare -A qwen2_5_32b_instruct=( ["model_name"]="qwen2.5-32b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )
declare -A qwen2_5_72b_instruct=( ["model_name"]="qwen2.5-72b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )

declare -A qwen_coder_32b_instruct=( ["model_name"]="qwen2.5-coder-32b-instruct" ["api_base"]=$aliyuncs_api_base ["api_key"]=$aliyuncs_api_key )

declare -A gpt_4o_mini=( ["model_name"]="gpt-4o-mini" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )
declare -A gpt_4o=( ["model_name"]="gpt-4o" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )
declare -A llama_3_1_70b=( ["model_name"]="llama-3.1-70b" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )
declare -A llama_3_1_8b=( ["model_name"]="llama-3.1-8b" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )
declare -A claude_3_5_sonnet_20241022=( ["model_name"]="claude-3-5-sonnet-20241022" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )
declare -A gpt_3_5_turbo=( ["model_name"]="gpt-3.5-turbo" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )
declare -A gemini_2_0_flash_exp=( ["model_name"]="gemini-2.0-flash-exp" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )
declare -A gemini_1_5_pro=( ["model_name"]="gemini-1.5-pro" ["api_base"]=$xiaohumini_api_base ["api_key"]=$xiaohumini_api_key )


question_file='data/question/test_v2_hard_50.jsonl'
version='test_v2_hard_50_v2'
language_type="en"

# declare -a bench_run_models=(qwen2_5_14b_instruct qwen2_5_3b_instruct qwen2_5_32b_instruct qwen2_5_72b_instruct)

# declare -a gen_result_models=(qwen_coder_32b_instruct gpt_4o_mini gpt_4o llama_3_1_70b llama_3_1_8b deepseek_chat claude_3_5_sonnet_20241022 gpt_3_5_turbo gemini_2_0_flash_exp gemini_1_5_pro deepseek_coder qwen2_5_1_5b_instruct qwen2_5_7b_instruct qwen2_5_32b_instruct qwen_coder_1_5b_instruct  qwen_coder_3b_instruct qwen_coder_7b_instruct qwen_coder_14b_instruct llama3_2_3b_instruct llama3_2_1b_instruct llama_3_3_70b_instruct phi_4 gemma_2_27b_it ministral_8b ministral_3b phi_3_5_mini_128k_instruct gemma_2_9b_it codestral_2501 gpt_4o_2024_11_20 gemini_exp_1206 llama_3_1_70b_instruct llama_3_1_8b_instruct qwen2_5_14b_instruct qwen2_5_3b_instruct qwen2_5_72b_instruct)

declare -a bench_run_models=(deepseek_chat claude_3_5_sonnet_20241022 gpt_4o_2024_11_20 gemini_exp_1206)

declare -a gen_result_models=(deepseek_chat claude_3_5_sonnet_20241022 gpt_4o_2024_11_20 gemini_exp_1206)


gen_result_models_names=""
for model in "${gen_result_models[@]}"; do
    declare -n modelRef=$model
    if [ -z "$gen_result_models_names" ]; then
        gen_result_models_names=${modelRef[model_name]}
    else
        gen_result_models_names="$gen_result_models_names,${modelRef[model_name]}"
    fi
done
echo "result Model Names: $gen_result_models_names"

function function_to_run {
    model_name=$1
    api_base=$2
    api_key=$3
    question_file=$4
    version=$5
    language_type=$6
    echo "Running function with parameters: $model_name, $api_base, $api_key, $question_file, $version, $language_type"
    . script/llm_gen_api.sh "$model_name" "$api_base" "$api_key" "$question_file" "$version" "$language_type"
    . script/llm_judge.sh "$model_name" "$version" "$language_type"
}
# 导出函数
export -f function_to_run

for model in "${bench_run_models[@]}"; do
    declare -n modelRef=$model
    printf "%s %s %s %s %s %s\n" "${modelRef[model_name]}" "${modelRef[api_base]}" "${modelRef[api_key]}" "$question_file" "$version" "$language_type"
done | parallel --ungroup --max-procs 4 --colsep ' ' function_to_run

. script/model_result.sh "$version" "$gen_result_models_names"


# screen -S bench_run
# conda activate lin_rany_11
# bash script/bench_run.sh > test_v2_hard_50_v2_1.log 2>&1