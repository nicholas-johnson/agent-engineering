import json
import urllib.request
from pathlib import Path

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

# What we need from a model. Change these and see what's left.
MAX_INPUT_PRICE = 0.50  # dollars per million input tokens
MIN_CONTEXT = 1_000_000  # tokens
NEEDS_IMAGES = True
NEEDS_OPEN_WEIGHTS = True

with urllib.request.urlopen("https://openrouter.ai/api/v1/models") as response:
    models = json.load(response)["data"]
print(f"OpenRouter lists {len(models)} models today\n")

matches = []
for model in models:
    input_price = float(model["pricing"]["prompt"]) * 1_000_000
    output_price = float(model["pricing"]["completion"]) * 1_000_000
    if input_price > MAX_INPUT_PRICE or model["context_length"] < MIN_CONTEXT:
        continue
    if NEEDS_IMAGES and "image" not in model["architecture"]["input_modalities"]:
        continue
    if NEEDS_OPEN_WEIGHTS and not model.get("hugging_face_id"):
        continue
    matches.append((input_price, output_price, model["id"], model["context_length"]))
matches.sort()

for input_price, output_price, model_id, context in matches:
    print(f"${input_price:6.3f} in  ${output_price:6.3f} out  {context:>9,} tokens  {model_id}")
print(f"\n{len(matches)} models match")

(OUTPUT / "catalogue.json").write_text(json.dumps(models, indent=2))
