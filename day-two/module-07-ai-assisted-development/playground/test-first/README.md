# Test first

Demo 4's agent planned first, then built, and wrote its tests along the way. Here the order is stricter, and it's checked in code. First the agent turns DOR-231's acceptance criteria into tests, and runs them to watch them fail, before any feature code exists. Then it writes the code until they pass, and in that step it isn't allowed to touch the tests. You'll see the test run before and after, and find out whether tests written first keep an agent honest.

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/test-first/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/test-first/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The agent works on a fresh copy of `data/project` in `playground/test-first/output/project`. A run takes about 30 model calls and took about a minute and a half. The tests it wrote in the first step are in `output/tests.diff`, every change is in `output/changes.diff`, and the whole conversation is in `output/transcript.json`.

---

**Test-driven development** is writing a test before the code it tests: watch it fail, write just enough code to make it pass, then tidy up. The failing run matters. A test that passes before the code exists isn't testing the code.

The script uses demo 4's agent in one conversation with two messages. Each step can only write to one folder, so the agent can't make a test pass by changing the test:

```python
WRITE_TESTS = """Don't build anything yet. First, write tests for every acceptance criterion in the ticket, in tests/.
Run them. The new tests should fail, because nothing is built yet. Check each one fails for the right reason,
and not because of a mistake in the test. Then reply with each test's name and the criterion it checks."""
BUILD = "The tests are written and failing. Now change the code in dormouse/ until every test passes."

run_agent(conversation, instructions, "tests")      # step 1: may only write in tests/
run_agent(conversation, instructions, "dormouse")   # step 2: may only write in dormouse/
```

In this run the agent put its tests in a new file, each with a docstring, so `unittest -v` shows the docstring in place of the test's name:

```text
1. Write the tests:

  list_files 
  read_file  dormouse/settings.py
  read_file  dormouse/warm_wake.py
  read_file  dormouse/pages.py
  list_files 
  read_file  tests/test_settings.py
  read_file  tests/test_warm_wake.py
  read_file  tests/test_pages.py
  write_file tests/test_dor_231.py
  run_tests  
  run_tests  
  write_file tests/test_dor_231.py
  run_tests  

Before: the tests, with no code written
    Acceptance: for 30, 60 or 90 minutes, heating is capped at that limit. ... 
    Acceptance: for 30, 60 or 90 minutes, heating is capped at that limit. ... FAIL
    Acceptance: for 30, 60 or 90 minutes, heating is capped at that limit. ... FAIL
    Acceptance: new and unchanged existing customers get 60 minutes. ... FAIL
    Acceptance: How early is visible only while Warm Wake is on. ... FAIL
    Acceptance: any other value for How early is rejected. ... ok
    Acceptance: page text uses the brand voice. ... FAIL
    Acceptance: both controls appear under Schedule and neither under Heating. ... FAIL
    test_every_setting_has_a_control ... ok
    test_sections_are_in_order ... ok
    test_switches_show_their_state ... ok
    test_warm_wake_is_under_heating ... ok
    test_boost_temperature_goes_in_half_degrees ... ok
    test_boost_temperature_has_a_range ... ok
    test_every_default_is_allowed ... ok
    test_switches_are_on_or_off ... ok
    test_unknown_setting_is_rejected ... ok
    test_update_checks_every_change ... ok
    test_update_returns_a_new_copy ... ok
    test_a_warm_room_needs_no_time ... ok
    test_minutes_to_heat ... ok
    test_never_more_than_90_minutes_early ... ok
    test_starts_early_by_the_time_the_home_takes_to_heat ... ok
    test_when_warm_wake_is_off_the_heating_starts_on_time ... ok
  Ran 22 tests: FAILED (failures=6)

2. Make them pass:

  read_file  dormouse/settings.py
  read_file  dormouse/warm_wake.py
  read_file  dormouse/pages.py
  read_file  tests/test_dor_231.py
  write_file dormouse/settings.py
  write_file dormouse/warm_wake.py
  write_file dormouse/pages.py
  run_tests  
  write_file dormouse/warm_wake.py
  run_tests  
  write_file dormouse/pages.py
  run_tests  
  write_file dormouse/warm_wake.py
  run_tests  
  write_file dormouse/pages.py
  run_tests  
  run_tests  
  run_tests  
  list_files 
  read_file  dormouse/warm_wake.py
  write_file dormouse/warm_wake.py
  read_file  dormouse/pages.py
  write_file dormouse/pages.py
  run_tests  

After:
    Acceptance: for 30, 60 or 90 minutes, heating is capped at that limit. ... ok
    Acceptance: new and unchanged existing customers get 60 minutes. ... ok
    Acceptance: How early is visible only while Warm Wake is on. ... ok
    Acceptance: any other value for How early is rejected. ... ok
    Acceptance: page text uses the brand voice. ... ok
    Acceptance: both controls appear under Schedule and neither under Heating. ... ok
    test_every_setting_has_a_control ... ok
    test_sections_are_in_order ... ok
    test_switches_show_their_state ... ok
    test_warm_wake_is_under_heating ... FAIL
    test_boost_temperature_goes_in_half_degrees ... ok
    test_boost_temperature_has_a_range ... ok
    test_every_default_is_allowed ... ok
    test_switches_are_on_or_off ... ok
    test_unknown_setting_is_rejected ... ok
    test_update_checks_every_change ... ok
    test_update_returns_a_new_copy ... ok
    test_a_warm_room_needs_no_time ... ok
    test_minutes_to_heat ... ok
    test_never_more_than_90_minutes_early ... FAIL
    test_starts_early_by_the_time_the_home_takes_to_heat ... ok
    test_when_warm_wake_is_off_the_heating_starts_on_time ... ok
  Ran 22 tests: FAILED (failures=2)

Agent: Implemented How early with a 60-minute default, validation for 30/60/90 minutes, and a cap on Warm Wake’s early start. Moved the controls to Schedule and made How early visible only when Warm Wake is on.

Ran `python -m unittest`, but it still reports two failures: the existing tests `test_warm_wake_is_under_heating` and `test_never_more_than_90_minutes_early` expect the previous behaviour, which conflicts with this ticket’s requested changes. I did not change those tests.

The tests it wrote are in playground/test-first/output/tests.diff, and every change in changes.diff
```

The agent writes different tests on each run. An earlier run wrote its tests into the three existing test files instead, failed 6 and errored 4 before, and finished with one failure: `test_never_more_than_90_minutes_early` again.

## Things to notice

- **The old tests were the problem, in both runs.** DOR-231 moves Warm Wake to Schedule and changes the default to 60, so two existing tests have to change. In step 1 the agent was allowed to change them and didn't; in step 2 it wasn't allowed, so it couldn't. It said so plainly rather than pretending. Demo 4's agent changed them as it went. Here the rule made the conflict visible, and left a person to decide.
- **One new test passed before anything was built.** "Any other value for How early is rejected" was `ok` in the first run, with no How early setting at all. `check("how_early", 45)` raises `ValueError` because `how_early` is an unknown setting, which is the error the test was waiting for. It passes for the wrong reason, and would never catch a bug in the new check. The instructions asked the agent to check every test fails for the right reason. It didn't catch this one.
- **A test can pass and miss the bug.** "New and unchanged existing customers get 60 minutes" builds an "existing customer" with `dict(DEFAULTS)`, which already has the new default in it. Look at `output/project/dormouse/warm_wake.py`: when a customer's settings have no `how_early`, it falls back to 90 minutes, not 60. Every new test passes, and existing customers would still get 90. Two of the [second-opinion](../second-opinion/) reviewers found the same kind of gap in demo 4's change.
- **It wrote code to match its own test's words.** The brand-voice test looks for the exact text "Starts the heating up to 60 minutes early". Step 2 made the explanation say whatever How early is set to, which passes when it's 60. A test that checks a sentence word for word tells you the sentence hasn't changed, not that it follows the voice.

## Try this

1. **Let it fix the old tests.** Add to `WRITE_TESTS`: "If an existing test checks behaviour the ticket changes, update it, and say which and why." Do the two failures go away? Did it change anything it shouldn't have?
2. **Let it change tests in step 2.** Change the check in `run_tool` so step 2 can write to `tests/` as well as `dormouse/`. Does it fix the two old tests properly, or make them pass some other way?
3. **Catch the false pass.** After step 1, run the tests and fail the run if any new test passes. You'll need to know which tests are new: compare `unittest -v` before and after step 1.
4. **Mutation testing, by hand.** After a run, break the code on purpose: make `check` allow 45, or change the default to 90. Run `python -m unittest` in `output/project`. Which bugs do the agent's tests catch, and which slip through?
5. **Tests from a different author.** Copy `data/project` somewhere, write the tests yourself from the ticket, point `PROJECT` at your copy, and skip step 1. Is the agent's code better or worse against your tests than against its own?
6. **Watch the cost.** Count the steps in each half. In both runs, step 2 ran the tests six or more times. Print `response.usage` and add it up: is test-first slower or cheaper than demo 4's plan-first?

## Questions

For discussion. There are no right answers.

- The agent stopped with two failing tests and said why. Would you rather it had changed them, stopped earlier and asked, or done what it did?
- A test passed before any code existed, and nobody noticed until a person read the output. Who checks the checks?
- Every new test passed, and existing customers would still get 90 minutes. What does "the tests pass" tell you, and what doesn't it?
- If an agent writes both the tests and the code, is that test-first, or is it marking its own homework?

## Further reading

- **Beck, K. (2002). _Test-Driven Development: By Example_. Addison-Wesley.** The book that named the red, green, refactor loop this script follows. Read Part I, a worked example in small steps, and notice how often Beck runs the tests to watch them fail.
- **Anthropic. "Best practices for Claude Code." _Claude Code documentation_.** [code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices). Look for the advice to ask for a failing test that reproduces a problem before asking for the fix, and to give the agent a way to check its own work.

## Rabbit holes

- **Real mutation testing.** [mutmut](https://github.com/boxed/mutmut) makes hundreds of small changes to your code (flipping `<` to `<=`, changing numbers) and runs your tests against each one. Point it at `output/project` after a run, and see what share of the agent's tests would notice a bug.
- **Test-first in a real agent.** In Claude Code or Cursor, in a copy of `data/project` (see `demo/LIVE.md`), ask for failing tests from DOR-231 first, check them yourself, commit them, and only then ask for the code. Does the tool respect "don't change the tests" when you only say it, without a rule in code to stop it?
