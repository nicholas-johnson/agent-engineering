---
name: test-plan
description: Write a manual test plan for a change, for QA to follow in the app and the web dashboard. Use when a ticket is ready for testing.
---

# Write a test plan

Work from the ticket and the change that implements it. If you weren't given them, ask which ticket it is, and read the change with `git diff`. Write a test plan that a tester can follow in the app and the web dashboard, without reading code.

- One numbered test per line of behaviour, each with **Steps** and **Expected result**.
- Cover every acceptance criterion, and say which one each test covers.
- Add the edge cases a customer could hit: turning features off and on again, existing customers after the update, values at the limits.
- Finish with a short list of what the automated tests in the change already cover, so the tester can skip it.

Plain British English. No more than 12 tests.
