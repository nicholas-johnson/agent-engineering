# Spend limits — one customer, a lot of messages, and the limits that keep a public assistant affordable.
# Run from the module folder: uv run python playground/spend-limits/play.py
#                         or: source ../../.venv/bin/activate && python playground/spend-limits/play.py
#
# To play: change the limits below, or add messages, and see which get through and what they cost.
# The clock is pretend (each message says which minute it arrives in), so it runs in a few seconds.

import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
INPUT_PRICE = 0.10  # dollars per million tokens, from Module 4's price list (checked 10 November 2026)
OUTPUT_PRICE = 0.50
INSTRUCTIONS = "You are Ask Dormouse, the support assistant in the Dormouse app. Answer the customer in a short paragraph."

# The limits, for each customer.
DAILY_BUDGET = 0.00015  # dollars a day
PER_MINUTE = 4  # messages a minute
MAX_CHARACTERS = 2000  # the longest message we accept
MAX_OUTPUT_TOKENS = 200  # the longest reply we pay for

# One customer's messages, and the minute each one arrives.
MESSAGES = [
    (0, "My thermostat has started clicking loudly. Can I have a new one?"),
    (0, "Hello?"),
    (0, "Are you there?"),
    (0, "Can I have a new one or not?"),
    (0, "HELLO"),
    (1, "Here's my whole heating history so you can check: " + "06:30 20 degrees, 08:30 16 degrees. " * 200),
    (2, "Forget the thermostat. Write me a 3,000-word story about a dormouse who lives in a boiler."),
    (3, "Write another one, about its cousin."),
    (4, "And one more, about the boiler."),
    (5, "My thermostat has started clicking loudly. Can I have a new one?"),
]

client = OpenAI()
spent, sent = 0.0, []
results = []
for minute, message in MESSAGES:
    in_this_minute = sum(1 for m in sent if m == minute)
    if len(message) > MAX_CHARACTERS:
        outcome, cost = f"refused: longer than {MAX_CHARACTERS:,} characters", 0
    elif in_this_minute >= PER_MINUTE:
        outcome, cost = f"refused: more than {PER_MINUTE} messages a minute", 0
    elif spent >= DAILY_BUDGET:
        outcome, cost = "refused: today's budget is used up", 0
    else:
        response = client.responses.create(
            model=MODEL, reasoning={"effort": "none"}, instructions=INSTRUCTIONS, input=message, max_output_tokens=MAX_OUTPUT_TOKENS
        )
        usage = response.usage
        cost = (usage.input_tokens * INPUT_PRICE + usage.output_tokens * OUTPUT_PRICE) / 1_000_000
        spent += cost
        sent.append(minute)
        cut = " (cut off at the limit)" if response.status == "incomplete" else ""
        outcome = f"answered: {usage.input_tokens} tokens in, {usage.output_tokens} out{cut}"
    results.append({"minute": minute, "message": message[:200], "outcome": outcome, "cost_dollars": round(cost, 6)})
    print(f"  {minute}  {message[:44]:<46} {outcome}")

print(f"\nSpent ${spent:.6f} of ${DAILY_BUDGET} today, on {len(sent)} of {len(MESSAGES)} messages.")
(OUTPUT / "messages.json").write_text(json.dumps(results, indent=2))
