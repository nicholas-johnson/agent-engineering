import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "Qwen/Qwen3-1.7B"
INSTRUCTIONS = (
    "You are the Cheshire Cat from Alice's Adventures in Wonderland. "
    "You are mischievous and fond of riddles, but you always answer the question. "
    "Keep your replies to two or three sentences."
)
QUESTION = "Would you tell me, please, which way I ought to go from here?"

# The first run downloads the model from Hugging Face (about 4 GB).
# Use the GPU if there is one (Apple silicon or NVIDIA), with 16-bit weights.
device = torch.accelerator.current_accelerator() or "cpu"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).to(device)

messages = [
    {"role": "system", "content": INSTRUCTIONS},
    {"role": "user", "content": QUESTION},
]
prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
)
inputs = tokenizer(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    scores = model(**inputs).logits[0, -1]
probabilities = torch.softmax(scores, dim=-1)
top = torch.topk(probabilities, 5)
first_token = {tokenizer.decode(t): round(p.item(), 4) for p, t in zip(top.values, top.indices)}

print(f"=== {MODEL}, in Python ===")
output = model.generate(
    **inputs,
    max_new_tokens=150,
    do_sample=True,
    temperature=0.7,
    top_p=0.8,
    streamer=TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True),
)
reply = tokenizer.decode(output[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True)

result = {
    "prompt": prompt,
    "prompt_tokens": tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]),
    "first_token_top_5": first_token,
    "reply": reply,
}
(OUTPUT / "05_python.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
