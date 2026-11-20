# Dormouse dashboard

The settings logic and the settings page of the Dormouse web dashboard.

## Commands

- Run the tests from this folder: `python -m unittest`. They must all pass before you finish.

## Code

- `dormouse/settings.py`: every setting, its default, and the values it allows.
- `dormouse/warm_wake.py`: when Warm Wake switches the heating on.
- `dormouse/pages.py`: the settings page, as HTML.
- `tests/`: one test file per module, using `unittest`.

## Rules

- Plain Python 3, standard library only.
- Every new setting needs a default, a check in `settings.check`, a row on the settings page, and tests.
- Change an existing test only when the change you were asked to make changes the behaviour it checks. Say which tests you changed, and why.
- Text that customers see is British English, in sentence case, in plain words. Feature names are capitalised: Warm Wake, Boost.
- Keep changes small. Don't reformat or rename code you weren't asked to change.
