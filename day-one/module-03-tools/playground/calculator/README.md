# Calculator

An agent with six maths tools: add, subtract, multiply, divide, power and square root. You'll ask questions that need several of them, and watch it plan the calculation.

From the module folder (`day-one/module-04-tools`):

```bash
uv run python playground/calculator/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/calculator/play.py
```

Needs `OPENAI_API_KEY` in `.env`. `play.py` starts `server.py` itself. The three conversations, with every tool call, are written to `playground/calculator/output/conversations.json`.

---

```text
You: A rectangle is 1,234.5 cm by 678.9 cm. How long is its diagonal?
  [tool] power({"base":1234.5,"exponent":2}) -> 1523990.25
  [tool] power({"base":678.9,"exponent":2}) -> 460905.20999999996
  [tool] add({"a":1523990.25,"b":460905.21}) -> 1984895.46
  [tool] square_root({"number":1984895.46}) -> 1408.863180014298
Agent: The diagonal is approximately 1,408.86 cm.
```

Pythagoras, in four tool calls, and nobody told it the formula.

## Things to notice

```text
You: What is 2 to the power of 100?
  [tool] power({"base":2,"exponent":100}) -> 1.2676506002282294e+30
Agent: 2 to the power of 100 is 1,267,650,600,228,229,401,496,703,205,376.
```

The tool returned a **floating-point** number, which keeps only about 17 significant digits. The agent's answer has 31. It is correct, but the last 14 digits did not come from the tool: the model knew them, because 2¹⁰⁰ is a famous number. With a less famous number it would have made them up. **Check where each digit in an answer came from.**

## Try this

1. **Your own questions.** Mortgage repayments, unit conversions, the area of a circle. Where does it chain tools well, and where does it do arithmetic in its head instead?
2. **Exact integers.** Change `power` so that, when both numbers are whole, it returns an exact integer (Python's `int` has no size limit). Ask for 2¹⁰⁰ and 3¹⁰⁰ again.
3. **Remove a tool.** Delete `square_root` from the server. How does the agent find a diagonal now? (Hint: `power` with an exponent of 0.5.)
4. **Without the instruction.** Remove "Use the tools for every calculation" from `INSTRUCTIONS`. Which calculations does it now do in its head? Are they right?
5. **One tool to rule them all.** Replace all six tools with one, `evaluate(expression: str)`, that works out an expression like `"1000 * 1.045 ** 17"`. Fewer calls? What could go wrong if you used Python's `eval` to do it?

## Questions

For discussion. There are no right answers.

- The agent filled in digits the tool never gave it. How would you make sure you know where every digit in an answer came from?
- Should an agent ever do arithmetic in its head, or always use a tool?
- Is one `evaluate(expression)` tool safer or riskier than six small tools? Why?

## Further reading

- **Singh, A. K. & Strouse, D. J. (2024). "Tokenization counts: the impact of tokenization on arithmetic in frontier LLMs."** [arXiv:2402.14903](https://arxiv.org/abs/2402.14903). A number is split into tokens like any other text, and where the split falls changes the arithmetic. Read it next to the digits the tool never returned.
- **Gao, L. et al. (2023). "PAL: Program-aided Language Models." *ICML 2023*.** [arXiv:2211.10435](https://arxiv.org/abs/2211.10435). Have the model write one short program for the whole problem, and run it. Compare it with the `evaluate(expression)` exercise.
