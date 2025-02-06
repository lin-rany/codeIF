#  bash script/if_pipeline.sh
chmod +x script/llm_gen_local.sh
chmod +x script/llm_gen_api.sh
chmod +x script/llm_judge.sh

export CUDA_VISIBLE_DEVICES="2"

#  local or api
type='api' 
model=gpt-4o

api_base=""
api_key=""

question_file='data/question/final_release_1200.jsonl'
version='default'


language_type='en'

. script/llm_gen_${type}.sh $model $api_base $api_key $question_file $version $language_type
. script/llm_judge.sh $model $version $language_type

. script/model_result.sh $version


