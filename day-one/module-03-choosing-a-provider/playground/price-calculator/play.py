import json
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

# A chatbot for a small company: 1,000 people, 20 messages each a working day.
USERS = 1000
MESSAGES_PER_DAY = 20
WORKING_DAYS_PER_MONTH = 21
INPUT_TOKENS_PER_MESSAGE = 1500  # instructions + conversation so far + the new message
OUTPUT_TOKENS_PER_MESSAGE = 200

prices = json.loads((DATA / "prices.json").read_text())
messages = USERS * MESSAGES_PER_DAY * WORKING_DAYS_PER_MONTH
input_millions = messages * INPUT_TOKENS_PER_MESSAGE / 1_000_000
output_millions = messages * OUTPUT_TOKENS_PER_MESSAGE / 1_000_000

rows = []
for model in prices["models"]:
    cost = input_millions * model["input_per_million"] + output_millions * model["output_per_million"]
    rows.append((cost, model["id"], model["country"], model["open_weights"]))
rows.sort()

print(f"{messages:,} messages a month, prices checked {prices['checked']}\n")
lines = ["monthly_cost,model,country,open_weights"]
for cost, model_id, country, open_weights in rows:
    print(f"${cost:>10,.2f}  {model_id:32} {country:8} {'open weights' if open_weights else ''}")
    lines.append(f"{cost:.2f},{model_id},{country},{open_weights}")

(OUTPUT / "monthly_costs.csv").write_text("\n".join(lines) + "\n")
