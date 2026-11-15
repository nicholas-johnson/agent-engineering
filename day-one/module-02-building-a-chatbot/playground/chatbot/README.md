# Chatbot

A complete streaming chatbot, with every setting at the top of the file. You'll chat with it, change a setting, and see what that does to the replies.

From the module folder (`day-one/module-02-building-a-chatbot`):

```bash
uv run python playground/chatbot/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/chatbot/play.py
```

Needs `OPENAI_API_KEY` in `.env`. Press Enter on an empty line to stop. The conversation is saved to `playground/chatbot/output/conversation.txt` after every turn.

---

It's the chatbot from the demos, ready to take apart.

```text
You: What is a token, in one sentence?
Bot: A token is a piece of text—such as a word, part of a word, or punctuation—that an AI model processes at a time.
```

## The settings

| Setting | Default | What it does |
|---------|---------|--------------|
| `MODEL` | `"gpt-6-luna"` | Which model answers. Try `"gpt-6-sol"` |
| `REASONING_EFFORT` | `"none"` | How much the model "thinks" before answering: `"none"`, `"low"`, `"medium"`, `"high"` |
| `TEMPERATURE` | `1.0` | How adventurous its word choices are, from 0 to 2 |
| `MAX_OUTPUT_TOKENS` | `500` | The longest reply it is allowed to write |
| `INSTRUCTIONS` | a helpful assistant | Who it is and how it behaves |

## Things to notice

- Set `REASONING_EFFORT = "low"` and you get an error: *"Unsupported parameter: 'temperature' is not supported with this model."* The model is fine. Temperature only works when reasoning effort is `"none"`, so delete the `temperature=` line too.
- Set `MAX_OUTPUT_TOKENS = 20` and ask for a story. The reply just stops mid-sentence.

## Try this

1. **Slash commands.** Make `/reset` clear the conversation, and `/model gpt-6-sol` switch model mid-chat.
2. **Show the cost.** After each reply, print the tokens it used. You'll need to catch the `response.completed` event, which carries `event.response.usage`.
3. **Pick up where you left off.** Save `messages` to a JSON file when you quit, and load it when you start, so the conversation carries on next time.
4. **Think first.** Switch to `REASONING_EFFORT = "medium"` (and remove the temperature). Ask a tricky question. Is it slower? Better?
5. **Let the API remember.** Instead of keeping `messages` yourself, pass `previous_response_id`. What do you still have to send, and what don't you?

## Questions

For discussion. There are no right answers.

- Who should choose the settings: the developer who builds the chatbot, or the person using it?
- If a reply is cut off by `MAX_OUTPUT_TOKENS` and the half-answer misleads someone, whose fault is it?
- When is it worth paying more, and waiting longer, for a model that thinks before it answers?

## Further reading

- **Ouyang, L. et al. (2022). "Training language models to follow instructions with human feedback." *NeurIPS 2022*.** [arXiv:2203.02155](https://arxiv.org/abs/2203.02155). InstructGPT, the ancestor of this chatbot. Figure 2 is how a next-token predictor was trained to answer a question rather than continue it.
- **OpenAI, [Text generation](https://developers.openai.com/api/docs/guides/text).** The settings at the top of `play.py` — model, instructions, temperature, length — as the API documents them.
