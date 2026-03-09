import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset

MODEL = 'Qwen/Qwen2.5-0.5B-Instruct'
OUTPUT_DIR = './mel_adapter'

print('⏳ Loading model...')
tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    torch_dtype=torch.float32,
    device_map='auto',
    trust_remote_code=True,
)

# ── Inject LoRA adapters ────────────────────────────────────────────
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,                  # rank — higher = more expressive, slower
    lora_alpha=32,        # scaling
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"],  # attention layers only
    bias="none",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # should be ~1% of total params

# ── Load & format training data ─────────────────────────────────────
with open('mel_training_data.json', 'r') as f:
    raw = json.load(f)

SYSTEM = "You are Mel. A chill friend. Short replies, real talk, no corporate speak."

def format_example(item):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": item["input"]},
        {"role": "assistant", "content": item["output"]},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False)
    return {"text": text}

formatted = [format_example(x) for x in raw]
dataset = Dataset.from_list(formatted)

def tokenize(example):
    result = tokenizer(
        example["text"],
        truncation=True,
        max_length=256,
        padding="max_length",
    )
    result["labels"] = result["input_ids"].copy()
    return result

tokenized = dataset.map(tokenize, remove_columns=["text"])

# ── Training args ───────────────────────────────────────────────────
args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=10,        # small dataset — more epochs needed
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=False,                 # keep off for Mac MPS stability
    logging_steps=5,
    save_strategy="epoch",
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized,
)

# ── Train ───────────────────────────────────────────────────────────
print('\n🔥 Training Mel...\n')
trainer.train()

# ── Save adapter only (tiny — few MB) ──────────────────────────────
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f'\n✅ Mel adapter saved to {OUTPUT_DIR}')