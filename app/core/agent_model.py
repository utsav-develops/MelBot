# app/core/agent_model.py
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

AGENT_MODEL = 'Qwen/Qwen2.5-1.5B-Instruct'

AGENT_SYSTEM = """You are a JSON extraction assistant.
You ONLY respond with raw valid JSON. 
No markdown. No explanation. No extra text.
Just the JSON object."""

agent_tokenizer = None
agent_model = None

def load_agent_model():
    global agent_tokenizer, agent_model

    print('⏳ Loading agent model...')

    agent_tokenizer = AutoTokenizer.from_pretrained(
        AGENT_MODEL,
        trust_remote_code=True
    )

    agent_model = AutoModelForCausalLM.from_pretrained(
        AGENT_MODEL,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map='auto',
        trust_remote_code=True,
    )

    agent_model.eval()
    print('✅ Agent model ready.')


def generate_structured(prompt: str) -> str:
    history = [
        {"role": "user", "content": prompt}
    ]

    messages = [{"role": "system", "content": AGENT_SYSTEM}] + history

    text = agent_tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = agent_tokenizer(text, return_tensors="pt").to(agent_model.device)

    # low temp for deterministic JSON output
    config = GenerationConfig(
        max_new_tokens=200,
        temperature=0.1,
        do_sample=True,
        repetition_penalty=1.1,
    )

    with torch.no_grad():
        output = agent_model.generate(**inputs, generation_config=config)

    reply = agent_tokenizer.decode(
        output[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    ).strip()

    return reply