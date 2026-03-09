from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from peft import PeftModel
import torch

BASE_MODEL = 'Qwen/Qwen2.5-0.5B-Instruct'
ADAPTER_DIR = './mel_adapter'
SYSTEM = "You are Mel. A chill friend. Short replies, real talk, no corporate speak."

tokenizer = None
model = None
gen_config = None

def load_model():
    global tokenizer, model, gen_config
    
    print('⏳ Loading Mel...')

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map='auto',
        trust_remote_code=True,
    )

    # model = PeftModel.from_pretrained(base, ADAPTER_DIR)

    model.eval()

    gen_config = GenerationConfig(
        max_new_tokens=150,
        temperature=0.9,
        repetition_penalty=1.3,
        do_sample=True,
    )

    print('✅ Mel ready.')


def generate(history: list) -> str:
    
    messages = [{"role": "system", "content": SYSTEM}] + history

    prompt = tokenizer.apply_chat_template(
        messages[-7:],
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(**inputs, generation_config=gen_config)

    reply = tokenizer.decode(
        output[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    ).strip()

    return reply
