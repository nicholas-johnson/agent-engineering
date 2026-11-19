---
title: Factory Reset and Re-Pair QA Report
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-10-31
---

# Factory Reset and Re-Pair QA Report

## Purpose and scope

This report defines the expected behaviour and verification steps for a factory reset followed by re-pairing on the Dormouse Thermostat with firmware 4.1. It covers removal of Wi-Fi details, schedules and the link to the Dormouse account, and confirms that the thermostat can be paired again after reset.

The reset procedure is intended for cases such as handing the thermostat to someone else or moving house without it. It returns the thermostat to its initial setup state. It does not change the hardware or resolve faults in the boiler, Wi-Fi network or thermostat sensors.

## Expected reset behaviour

To start a factory reset, hold the dial and boost button down together for 10 seconds, until the display shows RESET. The thermostat then restarts as if it were new.

After reset, the thermostat no longer has the previous Wi-Fi details, schedules or account link. The former account must not be treated as still connected to the reset thermostat. Pairing can then be started again using a Dormouse account and an available 2.4 GHz Wi-Fi network.

A reset removes the specified thermostat configuration. Do not describe it as removing household members, other devices or settings from other thermostats in the home: those behaviours are not defined by the user guide.

## Preconditions

Before testing, use a thermostat running firmware 4.1 and confirm its firmware at Menu > About. Record the hardware revision and serial prefix for the test record; hardware revisions A, B and C use serial prefixes DMA, DMB and DMC respectively.

Prepare:

- A Dormouse account with access to the thermostat.
- A 2.4 GHz Wi-Fi network with working internet access.
- The Dormouse app on a supported phone, signed in to the account.
- A thermostat with existing Wi-Fi pairing, a schedule and an account link.

The thermostat must be wired to the boiler by a qualified installer. Do not use a live heating installation as a reason to bypass safe working practices. During pairing, keep the phone within 5 metres of the thermostat.

## Test procedure

1. Confirm that the thermostat is paired and available in the app.
2. Confirm that schedules have been configured. The thermostat menu can show today's periods under Menu > Schedule; schedule changes are made in the app or web dashboard.
3. Hold the dial and boost button together for 10 seconds.
4. Verify that the display shows RESET.
5. Wait for the thermostat to restart.
6. Check that the previous account no longer has the thermostat linked as an available, connected thermostat.
7. Start pairing again: hold the dial down for 5 seconds until PAIR appears.
8. In the app, choose Add thermostat and follow the steps. Keep the phone within 5 metres until the app reports completion.
9. Confirm that pairing completes within 3 minutes of PAIR appearing.

Do not infer that reset is complete merely because the thermostat has restarted. Verify removal of each of the three specified items and verify a new pairing.

## Pass criteria

The test passes when all of the following are observed:

| Check | Pass condition |
|---|---|
| Reset initiation | RESET appears after the dial and boost button are held together for 10 seconds. |
| Wi-Fi details | The thermostat requires pairing to connect to Wi-Fi again; it does not reconnect using the former Wi-Fi details. |
| Schedules | The former schedules are no longer present after reset. |
| Account linkage | The former account link has been removed; pairing can be initiated as a new setup. |
| Re-pairing | The app completes pairing to a Dormouse account and 2.4 GHz network within 3 minutes of PAIR appearing. |
| Post-pairing operation | The app and thermostat show the newly paired thermostat as connected and available. |

Record the observed display messages, app outcome, firmware version, hardware revision and serial prefix. If a check cannot be confirmed, record it as inconclusive rather than passing it by assumption.

## Failure handling and known limits

If pairing takes longer than 3 minutes after PAIR appears, the display shows E-104. Start again by holding the dial for 5 seconds and keep the phone within 5 metres. Confirm that the selected network is 2.4 GHz; the thermostat cannot join a 5 GHz network.

If the display shows E-101, check that the router is on and offers a 2.4 GHz network. If the network name or password has changed, pair the thermostat again with the current details.

If the display shows E-110, the thermostat cannot reach the Dormouse cloud. Check that the router is connected to the internet. E-110 is not evidence that reset failed: the thermostat can keep running its schedules while disconnected, and app changes wait until it reconnects.

The guide does not specify a separate display confirmation for the removal of Wi-Fi details, schedules or account linkage. Verify those outcomes through the post-reset state and pairing behaviour rather than expecting an undocumented confirmation screen.

## Support and escalation

For user assistance, contact Dormouse support in the app under Help > Contact support. Provide the recorded firmware, hardware revision, test steps, display codes and whether Wi-Fi, schedule and account-link checks passed.

A failed re-pair should be investigated against the documented setup requirements and error-code guidance. Do not tell users that a reset has succeeded unless the reset sequence and its expected configuration removal have been verified. If the thermostat repeatedly fails the stated checks, document the behaviour for product investigation and avoid claiming that a further reset will correct an unrelated hardware, boiler or network fault.

## QA record

Complete one record per tested thermostat:

| Field | Result |
|---|---|
| Firmware version | |
| Hardware revision and serial prefix | |
| Previous pairing and schedule confirmed | |
| RESET displayed after button hold | |
| Wi-Fi details removed | |
| Schedules removed | |
| Account link removed | |
| New pairing completed within 3 minutes | |
| Error codes observed | |
| Overall result and notes | |
