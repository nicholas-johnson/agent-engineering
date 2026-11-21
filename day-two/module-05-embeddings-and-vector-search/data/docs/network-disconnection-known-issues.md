---
title: Network Disconnection Known Issues
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-05-15
---

# Network Disconnection Known Issues

## Scope

This internal note collects known reports involving Wi-Fi loss and cloud reachability on Dormouse Thermostats running firmware 4.1. It distinguishes E-101, which means the thermostat cannot find the Wi-Fi network, from E-110, which means it cannot reach the Dormouse cloud.

Use the displayed error code and the reported behaviour to classify an incident. Do not treat the codes as interchangeable: they identify different connection problems and have different user-visible effects.

## E-101: Wi-Fi network not found

E-101 means the thermostat cannot find its Wi-Fi network. The user-visible code is shown on the thermostat display and in the app. The thermostat requires a 2.4 GHz Wi-Fi network; it cannot join a 5 GHz network.

For an E-101 report, advise the user to check that the router is on and offers a 2.4 GHz network. If the network name or password has changed, the thermostat must be paired again.

Pairing procedure:

1. Hold the dial for 5 seconds, until the display shows PAIR.
2. In the app, choose Add thermostat and follow the steps.
3. Keep the phone within 5 metres of the thermostat until pairing finishes.

Pairing must finish within 3 minutes of PAIR appearing. If it does not, the thermostat shows E-104; the user must start pairing again. E-104 is a pairing timeout, not the E-101 network-not-found code.

## E-110: Dormouse cloud unreachable

E-110 means the thermostat cannot reach the Dormouse cloud. The user-visible code appears on the display and in the app. The thermostat keeps running its schedules while disconnected. Changes made in the app wait until the thermostat reconnects.

For an E-110 report, advise the user to check that the router is connected to the internet. Do not describe this code as a Wi-Fi network-not-found condition: the documented meaning is failure to reach the cloud.

Since firmware 3.2, E-110 is shown when the Dormouse cloud cannot be reached. Before that release, the Wi-Fi symbol flashed instead. This change affects the reported behaviour; it does not change the definition or response for E-101.

## Triage and support guidance

Start by recording the exact code shown on the thermostat and in the app, if available. Establish whether the report is E-101, E-110, or another code before giving connection guidance.

| Report | Meaning | Guidance |
|---|---|---|
| E-101 | Wi-Fi network not found | Check the router is on and offers 2.4 GHz Wi-Fi. If the network name or password changed, pair the thermostat again. |
| E-110 | Cannot reach the Dormouse cloud | Check that the router has an internet connection. Explain that schedules continue to run and app changes wait until reconnection. |
| E-104 | Pairing timed out | Restart pairing by holding the dial for 5 seconds; keep the phone within 5 metres and finish within 3 minutes. |

If the user needs further assistance, direct them to contact support in the app under Help > Contact support. Do not infer a fault or recommend a factory reset solely from an E-101 or E-110 report.

## Distinguishing user-visible behaviour

The documented difference between the two principal reports is the meaning of the code and, for E-110, the stated behaviour while the cloud is unreachable.

- **E-101:** the thermostat cannot find the Wi-Fi network. Check router power, 2.4 GHz availability, and whether network credentials have changed.
- **E-110:** the thermostat cannot reach the Dormouse cloud. Schedules continue; changes made in the app wait for reconnection.
- **E-104:** pairing did not finish in the required time. Restart the pairing process; this is not the same as either E-101 or E-110.

Do not promise that app changes will apply immediately during an E-110 incident. The documented behaviour is that they wait until the thermostat reconnects.

## Quality assurance checks

QA reports should preserve the user-visible distinction between Wi-Fi network discovery and cloud reachability. Check that support text and product behaviour identify E-101 as "Wi-Fi network not found" and E-110 as "Cannot reach the Dormouse cloud".

For E-110, verify that the documented guidance states that schedules keep running and app changes wait until reconnection. For E-101, verify that guidance calls out the 2.4 GHz requirement and the need to pair again if the network name or password has changed.

Also check that E-104 remains described as a pairing timeout, with the 3-minute completion window and 5-metre phone distance. Do not substitute E-104 for a network-loss or cloud-reachability code.

## Firmware and release context

The current firmware covered by the user guide is 4.1. The relevant change to cloud-reachability reporting arrived in firmware 3.2: E-110 began appearing when the Dormouse cloud could not be reached; previously, the Wi-Fi symbol flashed.

Firmware updates install automatically between 02:00 and 04:00 local time and cannot be postponed. During installation, the display shows UPDATING, the thermostat restarts, and heating pauses for about two minutes. If an update fails, the display shows E-510; the thermostat keeps its current firmware and tries again the next night.

## Internal rollout and test notes

Firmware is rolled out to 1% of thermostats, then 10%, then every thermostat over a week. Every release is tested against the manual test-script library before rollout.

When reviewing a network-disconnection report during a rollout, retain the firmware version and exact displayed code in the incident record. Use the user-visible definitions above when classifying it; do not infer that an update caused a connection issue from timing alone.
