# Vision

Point the model at a folder of pictures and ask it about each one.

```bash
uv run python play.py
```

It describes every image in `images/` (PNG, JPEG, WebP or GIF) and writes the descriptions to `output/descriptions.txt`. The folder starts with four of John Tenniel's illustrations from *Alice* ([Project Gutenberg #114](https://www.gutenberg.org/ebooks/114), public domain). Add your own.

```text
=== caterpillar.png ===
A large caterpillar sits on a giant mushroom, smoking a long pipe and facing a small girl. The scene is surrounded by oversized mushrooms and plants.

=== cat-fading.png ===
A person is curled up asleep on a thick tree branch, nestled among the leafy branches. The scene is rendered in a detailed black-and-white sketch.
```

## Things to notice

Open `images/cat-fading.png`. It is the Cheshire Cat disappearing into the leaves until only its grin is left. The model saw a person asleep on a branch, and said so with total confidence. Vision models can be **confidently wrong**, especially with unusual pictures.

## Try this

1. **Your own pictures.** Try a photo of your desk, a chart, a whiteboard, a page of handwriting, or a screenshot of an error message. Change `QUESTION` to suit.
2. **Ask it to read.** Give it a photo of a receipt or a sign. Can it read the text? Can it add up the receipt?
3. **Debug from a screenshot.** Take a screenshot of some code with a bug in it, and ask what's wrong.
4. **Give it a hint.** Change `QUESTION` to tell it the pictures are from *Alice in Wonderland*. Does it get `cat-fading.png` right now?
5. **Detail.** Each image part can take `"detail": "low"` or `"detail": "high"`. Try both on a picture with small text. How do the answers, and the input tokens, change?
6. **Compare two pictures.** Send two images in the same message and ask what's different between them.

## Questions

For discussion. There are no right answers.

- The model was completely confident, and completely wrong, about `cat-fading.png`. How would you design an app so that a confident wrong answer does less harm?
- Should a vision model describe the people in a photo: their age, their mood, who they might be? Where are the lines?
- Is a model's description of a picture easier or harder to check than its answer to a question? Why?
