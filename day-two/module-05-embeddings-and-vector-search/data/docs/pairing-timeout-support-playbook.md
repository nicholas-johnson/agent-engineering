---
title: Pairing Timeout Support Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-05-21
---

# Pairing Timeout Support Playbook

## Purpose and scope

Use this playbook when a Dormouse Thermostat displays E-104 during pairing. E-104 means pairing timed out: pairing must finish within 3 minutes of the display showing PAIR.

This playbook covers recovery steps and checks for support agents. It applies to the Dormouse Thermostat with firmware 4.1. Pairing connects the thermostat to the home Wi-Fi network and the customer's Dormouse account.

## Identify the timeout

Confirm that the display shows E-104, or that the app reports a pairing timeout. The app shows the same error code as the thermostat.

Before restarting, check that the customer is pairing with the Dormouse app and that their phone is within 5 metres of the thermostat. The phone must remain nearby until the app says pairing has finished.

Do not treat E-104 as a boiler fault. The error indicates that pairing did not complete within the allowed time.

## Recovery procedure

Guide the customer through these steps:

1. Hold the thermostat dial down for 5 seconds, until the display shows PAIR.
2. In the Dormouse app, choose Add thermostat and follow the pairing steps.
3. Keep the phone within 5 metres of the thermostat throughout pairing.
4. Wait for the app to say pairing has finished.

Pairing must finish within 3 minutes of PAIR appearing. If the display shows E-104 again, start the procedure from step 1. Each attempt requires a fresh pairing start.

## Support agent checks

If the customer is unsure whether pairing has restarted, ask them to confirm that the display shows PAIR after holding the dial for 5 seconds. Do not proceed based on an earlier pairing screen or a previous attempt.

Check that the phone stays within 5 metres until the app confirms completion. Moving the phone away before the app finishes does not meet the pairing instructions.

If the customer reports a different error code, use the guidance for that code rather than repeating the E-104 procedure. For example, E-101 indicates that the Wi-Fi network was not found; it is a different issue from a pairing timeout.

## Network and setup context

The thermostat requires a 2.4 GHz Wi-Fi network and cannot join a 5 GHz network. If E-101 appears, check that the router is on and offers a 2.4 GHz network. If the network name or password has changed, the thermostat must be paired again.

The customer needs the Dormouse app on a phone running Android 12 or later, or iOS 17 or later, and a Dormouse account. These are setup requirements, not specific causes of E-104. Keep the timeout recovery focused on restarting pairing and meeting the 3-minute and 5-metre requirements.

## Escalation and customer communication

If repeated attempts continue to end in E-104, verify that each attempt starts with the display showing PAIR, the app steps are followed, and the phone remains within 5 metres until completion. Do not promise that a retry will succeed or suggest that E-104 identifies a specific Wi-Fi, account or hardware fault.

For further help, direct the customer to contact Dormouse support in the app under Help > Contact support. Record that the reported code was E-104 and note which recovery checks were completed.

## Internal handling notes

Support has three levels:

| Level | Team |
|---|---|
| 1 | App chat agents |
| 2 | Product specialists |
| 3 | Engineering |

Use the established support process when a case needs escalation. The E-104 recovery steps in this playbook do not replace that process.

## QA reference

The recovery instructions must preserve these requirements:

- Hold the dial for 5 seconds until PAIR appears.
- Start pairing in the app using Add thermostat.
- Keep the phone within 5 metres until the app confirms completion.
- Finish within 3 minutes of PAIR appearing.
- If pairing times out, start again.

Do not shorten the time limit, change the phone-distance guidance, or imply that pairing is complete before the app confirms it.
