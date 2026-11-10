# Model catalogue

There are far more models than the 32 in `data/prices.json`. This downloads OpenRouter's public list of every model it offers, and filters it by what you need.

```bash
uv run python play.py
```

No API key needed. The filters are at the top of `play.py`. The full list, with every detail OpenRouter publishes about each model, is written to `output/catalogue.json`: search it.

The starting filters ask for an open-weight model that reads images, has a context window of at least a million tokens, and costs at most $0.50 per million input tokens:

```text
OpenRouter lists 469 models today

$ 0.000 in  $ 0.000 out  1,000,000 tokens  nvidia/nemotron-3.5-super-vl:free
$ 0.006 in  $ 0.500 out  1,048,576 tokens  deepseek/deepseek-v4.1-flash-1017
$ 0.040 in  $ 0.078 out  1,048,576 tokens  z-ai/glm-5.3-flash
$ 0.075 in  $ 0.300 out  1,048,576 tokens  minimax/minimax-m3.1-flash
$ 0.100 in  $ 0.300 out  1,310,720 tokens  meta-llama/llama-4-scout
...
19 models match
```

## Things to notice

- **Some models are free** (`:free`), usually with tight rate limits, and many are cheaper in **batch** (`:batch`), where you send work in bulk and wait for the answers instead of getting them straight away.
- **Look at the odd prices.** `deepseek-v4.1-flash-1017` charges $0.006 for input but $0.50 for output. Prices aren't always in proportion.

## Try this

1. **Your requirements.** Set the filters for a project of your own. How many models are left?
2. **Open `output/catalogue.json`.** Find a model and look at `supported_parameters`. Which models support `temperature`? Which have `reasoning`?
3. **Who has the most?** Count the models per lab (the part of the ID before the `/`). Which labs have the most models listed?
4. **Newest first.** Each model has a `created` timestamp. List the ten newest. How many were released this month?
5. **Speech and video.** Change the filter to models that take `audio` or `video` as input. Which labs offer them?
