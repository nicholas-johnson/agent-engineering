import datetime
import json
import urllib.request
from pathlib import Path

DATA = Path(__file__).parent
SOURCE = "https://openrouter.ai/api/v1/models"

LABS = {
    "openai": ("OpenAI", "USA"),
    "anthropic": ("Anthropic", "USA"),
    "google": ("Google", "USA"),
    "x-ai": ("xAI", "USA"),
    "meta": ("Meta", "USA"),
    "amazon": ("Amazon", "USA"),
    "deepseek": ("DeepSeek", "China"),
    "qwen": ("Alibaba (Qwen)", "China"),
    "moonshotai": ("Moonshot (Kimi)", "China"),
    "z-ai": ("Zhipu (GLM)", "China"),
    "minimax": ("MiniMax", "China"),
    "bytedance-seed": ("ByteDance", "China"),
    "baidu": ("Baidu", "China"),
    "tencent": ("Tencent", "China"),
    "xiaomi": ("Xiaomi", "China"),
    "mistralai": ("Mistral", "France"),
    "cohere": ("Cohere", "Canada"),
}

MODELS = [
    "openai/gpt-6-astra",
    "openai/gpt-6.1-sol",
    "openai/gpt-6.1-terra",
    "openai/gpt-6-luna",
    "anthropic/claude-fable-5.2",
    "anthropic/claude-opus-5.5",
    "anthropic/claude-sonnet-5.5",
    "anthropic/claude-haiku-5.5",
    "google/gemini-4-carbon",
    "google/gemini-4-argon",
    "google/gemini-3.8-flash",
    "google/gemini-3.5-flash-lite",
    "x-ai/grok-4.7",
    "x-ai/grok-build-0.1",
    "meta/muse-wonder",
    "meta/muse-spark-open",
    "amazon/nova-2-lite-v1",
    "deepseek/deepseek-v4-pro-0813",
    "deepseek/deepseek-v4.1-flash",
    "qwen/qwen3.8-max-0902",
    "qwen/qwen3.8-flash",
    "moonshotai/kimi-k3.1-pro",
    "z-ai/glm-5.3",
    "z-ai/glm-5.3-flash",
    "minimax/minimax-m3",
    "bytedance-seed/seed-2-1-turbo",
    "baidu/ernie-5.5-flash-preview",
    "tencent/hy4",
    "xiaomi/mimo-v2.6-pro",
    "mistralai/mistral-large-4-0",
    "mistralai/mistral-small-2603",
    "cohere/command-a-plus",
]

with urllib.request.urlopen(SOURCE) as response:
    catalogue = {model["id"]: model for model in json.load(response)["data"]}

models = []
for model_id in MODELS:
    model = catalogue[model_id]
    lab, country = LABS[model_id.split("/")[0]]
    models.append(
        {
            "id": model_id,
            "name": model["name"],
            "lab": lab,
            "country": country,
            "input_per_million": round(float(model["pricing"]["prompt"]) * 1_000_000, 4),
            "output_per_million": round(float(model["pricing"]["completion"]) * 1_000_000, 4),
            "context_window": model["context_length"],
            "open_weights": bool(model.get("hugging_face_id")),
            "inputs": model["architecture"]["input_modalities"],
        }
    )

prices = {"checked": datetime.date.today().isoformat(), "source": SOURCE, "models": models}
(DATA / "prices.json").write_text(json.dumps(prices, indent=2) + "\n")
print(f"Wrote {len(models)} models to prices.json")
