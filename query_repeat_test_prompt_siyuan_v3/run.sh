export REQUEST_INTERVAL_FOR_OPENAI=3 # 请求间隔，秒

<<EOF
============= AZURE 相关配置 =============
为确保安全，直接在bash窗口声明一下变量
    export AZURE_OPENAI_KEY=
    export AZURE_OPENAI_ENDPOINT=
EOF

#以下配置不涉及安全，可以直接声明
export AZURE_OPENAI_API_TYPE="azure"
export AZURE_OPENAI_MODEL="gpt-35-turbo-instruct" # 可选模型：gpt-35-turbo、gpt-35-turbo-instruct

#python main.py --model-name gpt-3.5-turbo --dataset gsm8k --api_key "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" --sample_num 5 --max_tokens 512
#python main.py --model-name gpt-3.5-turbo --dataset logiqa --api_key "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" --sample_num 5 --max_tokens 512 --learning_mode cot_qrepeat
#python main.py --model-name gpt-3.5-turbo --dataset aqua --api_key "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" --sample_num 5 --max_tokens 512 --learning_mode cot_qrepeat
#python main.py --model-name gpt-3.5-turbo-instruct --dataset BoolQ --api_key "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" --sample_num 5 --max_tokens 512
#python main.py --model-name gpt-3.5-turbo --dataset BoolQ --api_key "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" --sample_num 5 --max_tokens 512
#python main.py --model-name gpt-3.5-turbo --dataset OBQA --api_key "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" --sample_num 5 --max_tokens 512
#python main.py --model-name gpt-3.5-turbo --dataset ANLI --api_key "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" --sample_num 5 --max_tokens 512

<<EOF
#12-21
## zero_shot + query repeat
python main.py --model-name gpt-3.5-turbo-instruct --dataset drop_break --learning_mode zero_shot_cot --max_tokens 300 --zero_shot_prompt "Let's repeat the complete question. \"" --zero_shot_prompt_stage2 "Therefore, in arabic numerals, the answer is"

## standard + query repeat
python main.py --model-name gpt-3.5-turbo-instruct --dataset drop_break --learning_mode standard_rephrase_v1 --max_tokens 300

#Step5：
python main.py --model-name gpt-3.5-turbo-instruct --dataset drop_break --learning_mode cot --max_tokens 450
python main.py --model-name gpt-3.5-turbo-instruct --dataset drop_break --learning_mode cot_rephrase_v1 --max_tokens 600

#Step6:
#    Demo in GSM8K
## cot + query repeat
python main.py --model-name gpt-3.5-turbo-instruct --dataset gsm8k --learning_mode cot_rephrase_v1 --max_tokens 600
EOF

# 使用AZURE OPENAI
   # --sample_num 本次测试使用的样本数量，不添加该参数表示使用全部样本

python main.py --api_key $AZURE_OPENAI_KEY --api_base $AZURE_OPENAI_ENDPOINT --api_type $AZURE_OPENAI_API_TYPE \
               --model-name $AZURE_OPENAI_MODEL \
               --dataset gsm8k --learning_mode cot_rephrase_v1 --max_tokens 600	 --sample_num 5 
