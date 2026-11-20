# Second opinion

Demo 5 ran the review skill once, and you read one review. But a review from a model is a sample, not a verdict. Here the same skill reviews the same change three times: with `gpt-6-luna` and no reasoning, as in demo 5; with `gpt-6-luna` thinking hard first; and with a different company's model, Claude. You'll compare what each one says must be fixed, how long each took, and decide how many reviewers a change needs.

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/second-opinion/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/second-opinion/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The Claude review also needs `ANTHROPIC_API_KEY`; without it, that reviewer is skipped with a message and the other two still run. The three reviews run at the same time, and the run took about 45 seconds, nearly all of it waiting for the slowest. Each review is written in full to `playground/second-opinion/output/`, one file per reviewer, named after it.

---

Everything the reviewers see is the same as in demo 5: the review skill's instructions, then the ticket, the project's `AGENTS.md` and the change in `data/changes/DOR-231.diff`. Only the reviewer changes:

```python
REVIEWERS = {
    "gpt-6-luna-none": ("OPENAI_API_KEY", review_openai, "none"),
    "gpt-6-luna-high": ("OPENAI_API_KEY", review_openai, "high"),
    "claude-opus-5-5-medium": ("ANTHROPIC_API_KEY", review_claude, "medium"),
}
```

The last word is the **reasoning effort**: how much the model thinks before it answers. `"none"` answers straight away; `"high"` thinks for longer first. Claude Opus 5.5 always thinks a little, so `"medium"`, its default, is the setting there. The script prints how long each review took, the verdict and what must be fixed:

```text
Reviewing the change for DOR-231: 3/3 reviews back

=== gpt-6-luna-none (5 seconds) ===

- **Verdict:** Request changes.
- **Must fix:**
  - `dormouse/settings.py`: `how_early` accepts values equal to `30`, `60` or `90` without checking their type. For example, `30.0` passes validation, despite the setting allowing only the specified values as an integer choice. Reject non-integer values as well as booleans so invalid settings cannot be stored.
  - `tests/test_settings.py`: Add rejection tests for non-integer numeric values such as `30.0` and `60.0`; current tests do not catch the validation issue above.

=== gpt-6-luna-high (41 seconds) ===

## Verdict: Request changes

## Must fix
- **`dormouse/warm_wake.py`, `dormouse/pages.py`** — Existing saved settings from before this change may not contain `how_early`. `DEFAULTS` adds the value for new settings, but both functions access `settings["how_early"]` directly. Such customers will get a `KeyError` instead of the 60-minute default. Add a migration or ensure missing settings are filled from `DEFAULTS`, and test an old settings mapping without `how_early`.

=== claude-opus-5-5-medium (24 seconds) ===

- **Verdict:** Request changes

- **Must fix:**
  - **`dormouse/warm_wake.py`, `dormouse/pages.py`: existing customers may crash.** Both now read `settings["how_early"]` directly. An existing customer's saved settings will not contain `how_early`. If saved settings are not merged with `DEFAULTS` when they are loaded, `heating_start` and `settings_page` will raise `KeyError` for every existing customer. The diff shows nothing that fills in the default, such as a migration or a merge on load. The only test uses `DEFAULTS`, which already contains the key. The third acceptance criterion names existing customers explicitly. Show where saved settings get the 60-minute default. If nothing does, add that handling. Either way, add a test that starts from a settings dict without `how_early` and gets 60 minutes.

The full reviews are in playground/second-opinion/output/
```

Reviews change from run to run, so yours will find different things.

## Things to notice

- **All three said "Request changes", for different reasons.** The quick review's only must-fix was that `30.0` passes the check. The two that thought first both found something bigger: existing customers' saved settings won't have `how_early` in them, so the code may crash for them, and the ticket's third criterion names existing customers. The quick review marked that criterion **Met**: "the default is 60."
- **Thinking cost time.** The same model took 5 seconds without reasoning and 41 with it. Claude took 24. Every review is cheap next to a bug that reaches 240,000 homes, but not every change needs 41 seconds.
- **The full reviews differ more than the headlines.** Open them. Claude's "Should fix" has five items, including `30.0` (the quick review's must-fix), a missing test for the selected option, and the `AGENTS.md` rule that changed tests must be explained. `gpt-6-luna-high`'s "Should fix" is "None", and it calls the changed test "required". The quick review says the page text doesn't meet the brand voice; the other two say it does.
- **Agreement isn't proof.** Two reviewers found the existing-customer gap. That makes it more likely to be real, but two models trained on similar text can share a blind spot too. Here the gap is real: [test-first](../test-first/)'s agent made a similar mistake, and its own tests didn't catch it.

## Try this

1. **Run it again.** Run the script twice more. Does each reviewer find the same must-fix every time? Which is steadier: the quick one or the slow ones?
2. **More effort settings.** Add `"gpt-6-luna-low"` and `"gpt-6-luna-medium"` to `REVIEWERS`. Where does the existing-customer problem start to be found?
3. **A cheaper Claude.** Add a reviewer that calls `review_claude` with `"low"` effort, or change `CLAUDE` to `"claude-sonnet-5-5"` in a copy of the function. Is it as good for less?
4. **A bad change.** Make a copy of `DOR-231.diff` and break it: set the default back to 90, or delete the test for rejected values. Point `CHANGE` at your copy. Which reviewers notice?
5. **Merge the reviews.** Add a fourth call that reads all three reviews and writes one list of must-fix items, saying which reviewers found each. Does merging help, or does it just make the list longer?
6. **Review its own work.** Have `gpt-6-luna` write the change (run [permissions](../permissions/) or [test-first](../test-first/)), then point `CHANGE` at its `output/changes.diff`. Is a model gentler on code it wrote?

## Questions

For discussion. There are no right answers.

- The quick review approved a criterion the slower ones failed. If you only ever ran the quick one, how would you find out?
- Two reviewers agree and one doesn't. Is that a vote, or should one good catch outweigh two misses?
- A thinking review took eight times as long. Which changes deserve it, and who decides?
- If every change gets two AI reviews, what is the human reviewer for?

## Further reading

- **Zheng, L. et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." _NeurIPS 2023 Datasets and Benchmarks Track_.** [arXiv:2306.05685](https://arxiv.org/abs/2306.05685). How far a model's verdicts can be trusted. Look for how often the strongest judge agreed with people, and for the judges' known biases, before you treat two matching reviews as settled.
- **Panickssery, A., Bowman, S. R. & Feng, S. (2024). "LLM Evaluators Recognize and Favor Their Own Generations."** [arXiv:2404.13076](https://arxiv.org/abs/2404.13076). Models can recognise their own writing, and rate it higher. Read the introduction, then do Try this 6.

## Rabbit holes

- **Reviews in the pull request.** Claude Code's GitHub Action (`anthropics/claude-code-action`) and Codex's (`openai/codex-action`) post a review on every pull request. Set one up on a repository of your own with this review skill, and see how often you agree with it over a week.
- **Measure the reviewers.** Make ten copies of the diff, each with one known bug. Run every reviewer over all ten, three times each, and count what each one catches. That's an evaluation, and the only honest way to choose a reviewer.
