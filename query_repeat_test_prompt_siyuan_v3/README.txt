Step1：
    <!-- Tested with python 3.9 -->
    pip install -r requirements.txt

Step2：
    create openai_key.txt file in root folder and add your openai api-key (sk-***)

Step3：
    ## zero_shot
    python main.py --model-name code-davinci-002 --dataset multiarith --learning_mode zero_shot
    python main.py --model-name gpt-3.5-turbo-0301 --dataset drop_break --learning_mode zero_shot

    ## zero_shot + query repeat
    python main.py --model-name code-davinci-002 --dataset multiarith --learning_mode zero_shot_cot --zero_shot_prompt "Let's repeat the question. \"" --max_tokens 300
    python main.py --model-name gpt-3.5-turbo-0301 --dataset drop_break --learning_mode zero_shot_cot --max_tokens 300 --zero_shot_prompt "Let's repeat the complete question. \"" --zero_shot_prompt_stage2 "Therefore, in arabic numerals, the answer is"

Step4：
    ## standard
    python main.py --model-name code-davinci-002 --dataset multiarith --learning_mode standard --max_tokens 300

    ## standard + query repeat
    python main.py --model-name code-davinci-002 --dataset multiarith --learning_mode standard_rephrase_v1 --max_tokens 300
    python main.py --model-name gpt-3.5-turbo-0301 --dataset drop_break --learning_mode standard --max_tokens 150
    python main.py --model-name gpt-3.5-turbo-0301 --dataset drop_break --learning_mode standard_rephrase_v1 --max_tokens 300

Step5：
    ## cot
    python main.py --model-name code-davinci-002 --dataset multiarith --learning_mode cot --max_tokens 300
    ## cot + query repeat
    python main.py --model-name code-davinci-002 --dataset multiarith --learning_mode cot_rephrase_v1 --max_tokens 450
    python main.py --model-name gpt-3.5-turbo-0301 --dataset drop_break --learning_mode cot --max_tokens 450
    python main.py --model-name gpt-3.5-turbo-0301 --dataset drop_break --learning_mode cot_rephrase_v1 --max_tokens 600

Step6:
    Demo in GSM8K
    ## cot
    python main.py --model-name gpt-3.5-turbo-0301 --dataset gsm8k --learning_mode cot --max_tokens 450

    ## cot + query repeat
    python main.py --model-name gpt-3.5-turbo-0301 --dataset gsm8k --learning_mode cot_rephrase_v1 --max_tokens 600
