---
title: Account Sign-In and Recovery QA Report
product: app
type: internal
audience: internal
firmware: 4.1
updated: 2026-05-16
---

# Account Sign-In and Recovery QA Report

## Scope

This report records QA coverage for Dormouse account sign-in and recovery. It covers password length requirements, two-step verification and password reset links, including their single-use behaviour and 30-minute expiry.

The account is used in the Dormouse app and web dashboard. Sign-in uses an email address and password. Two-step verification adds a 6-digit code when a member signs in on a new phone or browser. The code is sent by email, or supplied by an authenticator app if the member has set one up.

## Requirements under test

| Area | Expected behaviour |
|---|---|
| Password length | A password must have at least 10 characters. |
| Two-step verification | When enabled, a sign-in on a new phone or browser requires a 6-digit code as well as the password. |
| Code delivery | The code is sent by email, or comes from the member's authenticator app if configured. |
| Password reset | A member can request a reset link from the sign-in screen using Forgot password? and their email address. |
| Link lifetime | A reset link works for 30 minutes. |
| Link use | A reset link can be used once only. An expired link requires a new reset link. |

The guide does not specify password character rules beyond minimum length, code expiry or retry limits. Tests must not treat behaviour for those cases as a documented product requirement.

## Test setup and evidence

Run tests against firmware 4.1 account services using the Dormouse app and web dashboard. Use controlled test accounts and verify results in both clients where the flow is available. For two-step verification, prepare one account with the feature off and another with it on. For code delivery coverage, use separate accounts or test configurations for email and authenticator-app delivery.

Record the client, account state, time of reset-link request, time of each link attempt and observed result. Do not include actual passwords, 6-digit codes or active reset links in QA evidence. Use redacted captures and test-account identifiers.

## Password length tests

1. Attempt to set or use a password containing fewer than 10 characters. Confirm the password is not accepted where password creation or change is available.
2. Attempt with exactly 10 characters. Confirm the password meets the documented minimum.
3. Attempt with more than 10 characters. Confirm it is accepted, subject to any other applicable product validation.
4. Sign in using a valid account password of at least 10 characters. Confirm sign-in succeeds when other required checks are satisfied.

Record the exact length and outcome, not the password itself. The product documentation establishes only a minimum of 10 characters; it does not define a maximum, required character classes or treatment of spaces. Raise unexpected behaviour in those areas as a clarification rather than marking it against an undocumented rule.

## Two-step verification tests

Enable two-step verification using Settings > Account > Two-step verification. Confirm the feature can be turned on for the test account.

With the feature enabled, sign in on a new phone or browser using the account email address and password. Confirm the flow requests a 6-digit code in addition to the password. Verify the email delivery path, then repeat with an authenticator app configured and confirm the code can be obtained from that app.

With the feature disabled, sign in on a new phone or browser and confirm the documented additional-code requirement is not applied. Also test an incorrect or missing code as a negative case, recording the observed result without assuming undocumented retry or lockout rules.

## Password reset tests

From the sign-in screen, choose Forgot password? and enter the test account email address. Confirm that a reset link is sent and that the link can be used to reset the password within 30 minutes of the request.

After a successful reset, try the same link again. Confirm it cannot be used a second time. Then request another link and attempt to use it after 30 minutes have elapsed. Confirm it has expired and cannot complete the reset. Request a new link and verify that the new link works within its own 30-minute window.

Use timestamps to demonstrate the expiry boundary. Do not infer a precise result at exactly 30 minutes unless that boundary has been explicitly specified for the test run. The documented requirement is that links work for 30 minutes and can be used once.

## Cross-client and regression coverage

Run the supported sign-in and reset flows in the app and web dashboard. Check that successful password reset permits sign-in with the new password and that the previous password no longer works. For accounts with two-step verification enabled, confirm the additional-code step remains in place after password reset.

Check recovery after an expired link by requesting a new one, as directed by the product behaviour. Confirm that using a consumed or expired link does not prevent a separately requested new link from being used. Record any difference between app and dashboard outcomes for investigation.

## Results and defect triage

For each case, record pass, fail or blocked, with the client, account configuration and timestamped evidence. A failure to enforce the 10-character minimum, a missing required 6-digit step, acceptance of a reset link more than once, or acceptance after its 30-minute validity period should be filed as a product defect.

Treat undocumented details, including code expiry, attempt limits, password complexity and exact expiry-boundary handling, as questions for product clarification rather than assumed acceptance criteria.

## Internal support and escalation notes

Support has three levels: Level 1 app chat agents, Level 2 product specialists and Level 3 engineering. Route reproducible failures with redacted evidence and the affected client and account state. Escalate defects that bypass the documented minimum password length, two-step verification requirement or reset-link single-use and expiry rules.

Do not attach live credentials, codes or reset links to tickets. If a reset link has expired, the documented recovery action is to ask for a new one.
