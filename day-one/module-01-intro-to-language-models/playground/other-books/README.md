# Other books

The letter model only knows the text it counted. You'll run it on *Through the Looking-Glass* and on Python code, and watch it write like whichever one it read.

From the module folder (`day-one/module-01-intro-to-language-models`):

```bash
uv run python playground/other-books/play.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/other-books/play.py
```

Each corpus gets three samples of 400 characters, written to `playground/other-books/output/<corpus>.txt`.

---

This runs the eight-letter model from demo 3 on three corpora:

| Corpus | Where it comes from |
|--------|---------------------|
| `alice` | `data/alice.txt` |
| `looking-glass` | `looking-glass.txt` in this folder: *Through the Looking-Glass*, Carroll's sequel, from [Project Gutenberg](https://www.gutenberg.org/ebooks/12) |
| `python` | Four modules from Python's own standard library (`argparse`, `calendar`, `shutil`, `textwrap`), read from your Python installation |

This time the text keeps its capital letters, line breaks and indentation, because code needs them.

```text
=== python ===
    def itermonthdays(year, month):
            super(_AppendAction, self).__init__
               if logger is not specified year as a multi-line).
        func = format

    def __call__(self, heading = (
        ]
        return parser
```

It has no idea what Python is. It has just counted which character comes after every eight characters of code. Indentation, `self`, brackets and `return` all come for free.

## Try this

1. **Mash-up.** Join *Alice* and *Through the Looking-Glass* into one corpus. Then try *Alice* and the Python code. Where does it switch from one to the other?
2. **Your own writing.** Paste in a few thousand words of your own emails, notes or code. Does it sound like you? How much text does it need?
3. **Window size.** Try `WINDOW = 4` and `WINDOW = 12` on the Python corpus. When does it stop looking like code? When does it start copying whole functions?
4. **Another language.** Download a book in French or German from Project Gutenberg. Does the letter model care which language it is?
5. **More code.** Use every `.py` file in the standard library folder instead of four. Does the code get more convincing? How long does it take, and how big does the model get?

## Questions

For discussion. There are no right answers.

- The letter model wrote convincing-looking Python without knowing what Python is. How much of what looks like understanding in a big model could be the same trick?
- If a model trained on your emails writes just like you, whose writing is it?
- Where is the line between a model being influenced by a book and copying it?

## Further reading

- **Karpathy, A. (2015). "The Unreasonable Effectiveness of Recurrent Neural Networks."** [karpathy.github.io/2015/05/21/rnn-effectiveness](https://karpathy.github.io/2015/05/21/rnn-effectiveness/). A letter model trained on Shakespeare, Wikipedia, LaTeX and the Linux source, writing in the style of each. The same experiment as this playground, with a neural net in place of the counts.
