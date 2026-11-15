# Run from the module folder: uv run python demo/02_function.py

import math
from pathlib import Path

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)


def square_root(number: float) -> float:
    """Return the square root of a number, exactly, to full precision."""
    return math.sqrt(number)


answer = square_root(7654321)
print(f"square_root(7654321) = {answer:.10f}")

(OUTPUT / "02_function.txt").write_text(f"square_root(7654321) = {answer!r}\n")
