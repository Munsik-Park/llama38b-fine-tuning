import yaml
import torch
from pathlib import Path
from datasets import load_dataset, concatenate_datasets
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType

# 🔧 config 파일 로드
with open("configs/tinyllama.yaml", "r") as f:
    cfg = yaml.safe_load(f)

# 📦 모델과 토크나이저
model_id = cfg["model"]["base_model"]
tokenizer = AutoTokenizer.from_pretrained(cfg["tokenizer"]["tokenizer_name"])

# 토크나이저 설정 적용
tokenizer.padding_side = cfg["tokenizer"]["padding_side"]
tokenizer.truncation_side = cfg["tokenizer"]["truncation_side"]

# 패딩 토큰이 없으면 EOS 토큰을 패딩 토큰으로 사용
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if cfg["training"]["fp16"] else torch.float32,
    device_map="auto" if torch.cuda.is_available() else None
)

# LoRA 설정 적용
if cfg["model"]["use_lora"]:
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=cfg["model"]["lora_r"],
        lora_alpha=cfg["model"]["lora_alpha"],
        lora_dropout=cfg["model"]["lora_dropout"],
        target_modules=cfg["model"]["lora_target_modules"],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

# 📁 JSONL 데이터셋 로딩
jsonl_dir = Path(cfg["dataset"]["train_jsonl_dir"])
jsonl_files = list(jsonl_dir.glob("*.jsonl"))
assert jsonl_files, f"No JSONL files found in {jsonl_dir}"

print(f"Found {len(jsonl_files)} JSONL files")

datasets = [load_dataset("json", data_files=str(f), split="train") for f in jsonl_files]
dataset = concatenate_datasets(datasets)

print(f"Total dataset size: {len(dataset)}")

# 📄 텍스트 포맷 함수 - 실제 데이터 형식에 맞게 수정
def format_record(example):
    # 실제 데이터는 text 필드에 있음
    if "text" in example:
        return example["text"]
    elif "messages" in example:
        return tokenizer.apply_chat_template(example["messages"], tokenize=False)
    elif "input" in example and "output" in example:
        return f"{example['input']}\n###\n{example['output']}"
    else:
        raise ValueError(f"지원되지 않는 데이터 형식입니다. Available keys: {list(example.keys())}")

# 데이터 샘플 확인
print("Sample data format:")
sample = dataset[0]
print(f"Keys: {list(sample.keys())}")
print(f"Text preview: {sample.get('text', 'N/A')[:100]}...")

dataset = dataset.map(lambda x: {"text": format_record(x)})

# ✂️ 토크나이징
tokenized_dataset = dataset.map(
    lambda x: tokenizer(
        x["text"],
        padding="max_length",
        truncation=True,
        max_length=cfg["dataset"]["max_seq_length"],
        return_tensors=None  # 배치 처리를 위해 None으로 설정
    ),
    batched=True,
    remove_columns=dataset.column_names,
)

print(f"Tokenized dataset size: {len(tokenized_dataset)}")

# 🛠️ 학습 설정
args = TrainingArguments(
    output_dir=cfg["training"]["output_dir"],
    per_device_train_batch_size=int(cfg["training"]["per_device_train_batch_size"]),
    gradient_accumulation_steps=int(cfg["training"]["gradient_accumulation_steps"]),
    num_train_epochs=float(cfg["training"]["num_train_epochs"]),
    learning_rate=float(cfg["training"]["learning_rate"]),
    weight_decay=float(cfg["training"]["weight_decay"]),
    warmup_steps=int(cfg["training"]["warmup_steps"]),
    lr_scheduler_type=cfg["training"]["lr_scheduler_type"],
    fp16=bool(cfg["training"]["fp16"]),
    logging_dir="./logs",
    logging_steps=int(cfg["training"]["logging_steps"]),
    save_steps=int(cfg["training"]["save_steps"]),
    save_total_limit=int(cfg["training"]["save_total_limit"]),
    # evaluation_strategy=cfg["training"]["evaluation_strategy"],  # 평가 데이터셋이 없으므로 제거
    dataloader_num_workers=int(cfg["training"]["dataloader_num_workers"]),
    seed=int(cfg["training"]["seed"]),
    report_to="none",
    remove_unused_columns=False,  # PEFT 모델을 위해 필요
)


# 📦 Trainer
trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
)

# 🚀 Train
if __name__ == "__main__":
    print("🚀 Start training...")
    print(f"Model: {model_id}")
    print(f"Dataset size: {len(dataset)}")
    print(f"Max sequence length: {cfg['dataset']['max_seq_length']}")
    print(f"Batch size: {cfg['training']['per_device_train_batch_size']}")
    print(f"Gradient accumulation: {cfg['training']['gradient_accumulation_steps']}")
    print(f"Effective batch size: {cfg['training']['per_device_train_batch_size'] * cfg['training']['gradient_accumulation_steps']}")
    
    trainer.train()
    
    # 모델 저장
    if cfg["model"]["use_lora"]:
        trainer.save_model()
        print("✅ LoRA model saved.")
    else:
        trainer.save_model()
        print("✅ Full model saved.")
    
    print("✅ Training complete.")
