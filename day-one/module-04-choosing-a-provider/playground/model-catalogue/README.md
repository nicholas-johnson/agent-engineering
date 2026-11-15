# Model catalogue

OpenRouter's full list of models. You'll filter it by price, context length, inputs and whether the weights are open.

From the module folder (`day-one/module-03-choosing-a-provider`):

```bash
uv run python playground/model-catalogue/play.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/model-catalogue/play.py
```

No API key needed (requires an internet connection). The full list, with every detail OpenRouter publishes about each model, is written to `playground/model-catalogue/output/catalogue.json`: search it.

---

The filters are at the top of `play.py`. The starting filters ask for an open-weight model that reads images, has a context window of at least a million tokens, and costs at most $0.50 per million input tokens:

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
2. **Open `playground/model-catalogue/output/catalogue.json`.** Find a model and look at `supported_parameters`. Which models support `temperature`? Which have `reasoning`?
3. **Who has the most?** Count the models per lab (the part of the ID before the `/`). Which labs have the most models listed?
4. **Newest first.** Each model has a `created` timestamp. List the ten newest. How many were released this month?
5. **Speech and video.** Change the filter to models that take `audio` or `video` as input. Which labs offer them?

## Questions

For discussion. There are no right answers.

- With hundreds of models to choose from, what would you filter on first, and why?
- Why would a company give a model away for free?
- Many of the cheapest models have open weights. Why might an open model be cheaper to use than a closed one?

## Further reading

- **Liesenfeld, A. & Dingemanse, M. (2024). "Rethinking open source generative AI: open washing and the EU AI Act." *FAccT 2024*, 1774–1787.** [doi:10.1145/3630106.3659005](https://doi.org/10.1145/3630106.3659005). They score "open" models on what is actually shared: weights, data, code, documentation, licence. Read it before trusting an openness filter.
- **Solaiman, I. (2023). "The Gradient of Generative AI Release: Methods and Considerations." *FAccT 2023*.** [arXiv:2302.04844](https://arxiv.org/abs/2302.04844). Figure 1. Release runs from fully closed, to an API, to downloadable weights, to fully open. The catalogue's openness column is one point on that line.

## Rabbit holes

Optional. These leave the script.

1. **One whole record.** Open `catalogue.json` and pick a single model. Explain every key: `architecture` (what it can read and write), `pricing` (more than the two prices the script prints), `supported_parameters`, `hugging_face_id`.
2. **Suffixes that are not in the file.** OpenRouter's [model variants](https://openrouter.ai/docs/guides/routing/model-variants/overview). `:free` and `:batch` are separate catalogue entries. `:floor` and `:exacto` only change which provider serves the request, so they never appear in `catalogue.json`.
