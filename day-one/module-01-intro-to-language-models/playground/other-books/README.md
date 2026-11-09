# Other books

The model doesn't know anything about *Alice*. It only knows the text it counted. Give it different text and it writes like that instead.

This runs the eight-letter model from demo 3 on three corpora:

| Corpus | Where it comes from |
|--------|---------------------|
| `alice` | `data/alice.txt` |
| `looking-glass` | `looking-glass.txt` in this folder: *Through the Looking-Glass*, Carroll's sequel, from [Project Gutenberg](https://www.gutenberg.org/ebooks/12) |
| `python` | Four modules from Python's own standard library (`argparse`, `calendar`, `shutil`, `textwrap`), read from your Python installation |

```bash
uv run python play.py
```

This time the text keeps its capital letters, line breaks and indentation, because code needs them. Each corpus gets three samples of 400 characters, written to `output/<corpus>.txt`.

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
