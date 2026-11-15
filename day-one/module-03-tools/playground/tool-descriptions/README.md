# Tool descriptions

A tool's description is all the model knows about it. You'll give the model the same square root function three times, each time with a different description.

From the module folder (`day-one/module-04-tools`):

```bash
uv run python playground/tool-descriptions/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/tool-descriptions/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The results are written to `playground/tool-descriptions/output/results.json`.

---

There's no MCP server here: tools are defined straight in the Responses API, which is all MCP was doing for us. The same function is offered three times:

| Label | Description |
|-------|-------------|
| `clear` | "Return the square root of a number, exactly, to full precision." |
| `vague` | "Does a calculation." |
| `wrong` | "Returns the cube root of a number." |

```text
=== clear: "Return the square root of a number, exactly, to full precision." ===
Used the tool: yes
Agent: The square root of 7,654,321, to 10 decimal places, is 2766.6443573398.

=== vague: "Does a calculation." ===
Used the tool: yes
Agent: The square root of 7,654,321, rounded to 10 decimal places, is 2766.6443573398.

=== wrong: "Returns the cube root of a number." ===
Used the tool: yes
Agent: The square root of 7,654,321, to 10 decimal places, is 2766.6443573398.
```

## Things to notice

We expected the vague and wrong descriptions to stop the model using the tool. They didn't. With only one tool, the model calls it anyway, and then trusts whatever comes back over what the description said: it was told the tool returns cube roots, received a square root, and reported a square root.

So descriptions matter less than you might think when there's one obvious tool, and **results matter more**. Descriptions start to matter when the model has to choose: between several tools, or between using a tool and answering from memory. Try this to see it.

## Try this

1. **Give it a choice.** Add a second tool, `cube_root`, and give both tools vague descriptions. Which one does it pick? Now give them clear descriptions.
2. **Make it decide.** Ask a question that doesn't need a tool at all ("What is the capital of France?"). Does it ever call the tool anyway?
3. **Names matter too.** Rename the function from `calculate` to `square_root`, and keep the vague description. Does the name do the work the description wasn't doing?
4. **Describe the arguments.** Add `"description": "The number to take the square root of"` to the `number` property. Does anything change?
5. **Tell it when not to.** Write a description that says when *not* to use the tool, for example "Only for numbers over a million". Ask for the square root of 49.

## Questions

For discussion. There are no right answers.

- The model trusted what the tool returned over what its description said. Is that a good habit or a bad one?
- Who is a tool's description written for: the model, or the people who read the code? Can it be both?
- If a tool's description is wrong and something goes badly, whose fault is it?

## Further reading

- **Patil, S. G., Zhang, T., Wang, X. & Gonzalez, J. E. (2023). "Gorilla: Large Language Model Connected with Massive APIs."** [arXiv:2305.15334](https://arxiv.org/abs/2305.15334). Asked to call real APIs, models often name ones that were never published. Gorilla trains a model on the documentation. Look for how much a written description does once the model has to choose.
- **OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling).** The `description` on a tool and on its arguments. That text is all the model is shown.
