# Personas

The same model, the same question, completely different answers. The only thing that changes is the **instructions**.

```bash
uv run python play.py
```

Pick a persona from the list, then chat. Each persona is a short text file in `instructions/`. The conversation is saved to `output/<persona>.txt`.

| Persona | Instructions, in short |
|---------|------------------------|
| `cheshire-cat` | Mischievous and fond of riddles, but always answers |
| `grumpy-sysadmin` | Correct, practical, blunt and sarcastic |
| `haiku-poet` | Replies only in haiku |
| `pirate` | Calls you "matey", turns everything into a sea story |
| `socratic-tutor` | Never gives the answer, only questions that lead you there |

```text
You are talking to: pirate

You: How do I reverse a list in Python?
pirate: Arrr, matey! To reverse a list in place, use `my_list.reverse()`—it changes the original list. To make a reversed copy instead, sail with `reversed_list = my_list[::-1]`.
```

## Things to notice

Ask the `socratic-tutor` the same question:

```text
socratic-tutor: Do you want to reverse the list in place, or create a reversed copy? Have you tried `my_list.reverse()` or `my_list[::-1]`?
```

It was told never to give the answer, and it gave the answer anyway, just phrased as a question. **Instructions are strong suggestions, not rules.** The model is predicting what a helpful reply looks like, and sometimes being helpful wins.

## Try this

1. **Write your own.** Add a new `.txt` file to `instructions/`. A Shakespearean actor? A very cautious lawyer? A dog?
2. **Break character.** Try to get the `haiku-poet` to reply in prose, or the `pirate` to talk normally. Which personas are hardest to break? Then rewrite the instructions to make them harder to break.
3. **Fix the tutor.** Rewrite `socratic-tutor.txt` so it really never gives the answer, even when you beg.
4. **Two personas, one conversation.** Write a script where the `pirate` and the `cheshire-cat` talk to each other for ten turns. Each one's reply becomes the other's next message.
5. **How short can it be?** What is the shortest set of instructions that still produces a convincing persona?

## Questions

For discussion. There are no right answers.

- The tutor was told never to give the answer, and gave it anyway. Should a model follow instructions to the letter, or use its judgement? When would each be dangerous?
- Is a persona a kind of lie? When is it fine for a chatbot to pretend to be someone, and when isn't it?
- Many companies give their chatbots names and personalities. What should the people talking to them be told?
