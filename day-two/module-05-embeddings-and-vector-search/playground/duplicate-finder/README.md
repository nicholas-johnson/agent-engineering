# Duplicate finder

A library of 1,000 test scripts, written by different people over years, collects duplicates: the same check written twice, so it is run twice. You'll compare every script with every other script on the same platform and list the pairs that are almost the same.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/duplicate-finder/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/duplicate-finder/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds the library and keeps the vectors in `playground/duplicate-finder/output/vectors.db`. Every pair it finds is written to `playground/duplicate-finder/output/duplicates.json`, with both titles and expected results so you can judge them.

---

This is search turned on itself. Each script is embedded the way the demos do it (title + expected result), and then every script is compared with every other script on its platform: about 128,000 pairs. Android and iOS versions of the same test are meant to exist, so pairs across platforms are skipped. Any pair with a cosine similarity of at least `THRESHOLD = 0.90` is a possible duplicate.

```text
12 pairs of scripts on the same platform are at least 0.9 similar. The closest:

  0.994  web
    TS-1071  Reject a target below the supported range
    TS-1734  Reject a target above the supported range

  0.961  ios
    TS-1113  Raise target by one half-degree
    TS-1324  Lower target by one half-degree

  0.960  device
    TS-1473  Check temperature reading at lower display limit
    TS-1495  Check temperature reading at upper display limit

  0.942  device
    TS-1387  Rotate dial to raise the target temperature
    TS-1544  Rotate dial to lower the target temperature

  0.929  device
    TS-1552  Check humidity display at humid-room conditions
    TS-1995  Check humidity display at dry-room conditions
```

## Things to notice

- **The closest pairs aren't duplicates. They're mirror images.** Below and above, raise and lower, humid and dry. Each pair tests the two ends of the same thing. The embedding sees "the same kind of test" and, as in the similarity explorer, barely notices the one word that flips it. TS-1071 and TS-1734 even have word-for-word the same expected result, so the only difference left is "below" and "above" in the title.
- **The real duplicates are further down.** In `output/duplicates.json`, TS-1122, TS-1673 and TS-1832 all check that a humidity sensor fault shows E-221, with almost the same expected result (0.917 and 0.909). TS-1289 and TS-1332 both check E-217 for a disconnected temperature sensor (0.907). Those are the ones worth merging.
- **The threshold gives you a reading list, not an answer.** Twelve pairs is an afternoon's review for one person. Somebody still has to read each pair and decide.

## Try this

1. **Move the threshold.** Try 0.85, then 0.80. How many pairs do you get? At what point are most of them not duplicates?
2. **Across platforms.** Remove the platform check. Which pairs score 1.000, and are they duplicates?
3. **Embed the full text.** Use the title, preconditions, steps and expected result instead. Do the mirror-image pairs move up or down?
4. **Groups, not pairs.** TS-1673 is in two pairs. Merge pairs that share a script into groups, so that if A is like B and B is like C, all three are listed together.
5. **Ask a model.** Send each pair to `gpt-6-luna` and ask: the same test, opposite cases of one test, or different tests? Compare its answers with yours.
6. **Find the missing mirror.** Look for a script with no partner: a "below the minimum" test on a platform that has no "above the maximum" test. A gap in a test library is often worth more than a duplicate.

## Questions

For discussion. There are no right answers.

- The closest pairs were opposites. Should "reject a target below the range" and "reject a target above the range" be one test or two?
- If a tool deleted every pair above 0.90 automatically, what would be lost?
- Who should decide that two tests are duplicates: the people who wrote them, the people who run them, or whoever owns the product?
- Which threshold would you pick, and how would you explain the choice to your team?
