import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from peft import PeftModel, PeftConfig

# 🔧 설정
lora_path = "outputs/tinyllama-finetune"  # LoRA 경로
device = "cuda" if torch.cuda.is_available() else "cpu"

# 🔌 로딩
config = PeftConfig.from_pretrained(lora_path)
base_model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path).to(device)
model = PeftModel.from_pretrained(base_model, lora_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)

# 📝 채팅 템플릿 적용 여부
USE_CHAT_TEMPLATE = hasattr(tokenizer, "apply_chat_template")

# 스트리머
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

# 📣 CLI 루프
print("💬 TinyLLaMA LoRA CLI (종료하려면 'exit' 입력)")
while True:
    prompt = input("🙋 사용자 질문: ")
    if prompt.strip().lower() in ["exit", "quit", "q"]:
        break

    if USE_CHAT_TEMPLATE:
        messages = [{"role": "user", "content": prompt}]
        prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    else:
        prompt_text = prompt

    inputs = tokenizer(prompt_text, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=True,
            top_p=0.95,
            temperature=0.7,
            repetition_penalty=1.1,
            streamer=streamer
        )
