---
title: Temperature Sensor Fault Escalation Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-09-14
---

# Temperature Sensor Fault Escalation Playbook

## Purpose and scope

This internal playbook covers support handling when a Dormouse Thermostat reports E-217, Temperature sensor disconnected. Use it to guide the customer-facing response and the escalation to arrange a replacement through support.

E-217 is a safety-related fault. The thermostat turns the heating off to be safe. Do not describe the heating as continuing to operate normally while this code is present, and do not advise a customer to bypass the shutdown.

The code appears on the thermostat display and in the app. The app can also notify the customer about the error. The immediate priority is to explain the shutdown clearly and help the customer contact Dormouse support.

## Confirm the reported fault

Confirm that the displayed or reported code is E-217. The thermostat and app show the same error code, so either can be used to identify the fault.

Keep the diagnosis tied to the reported code. E-217 means the temperature sensor is disconnected; the prescribed action is to contact Dormouse support to arrange a replacement. Do not treat it as a Wi-Fi, boiler-response, battery or firmware-update problem.

If the customer reports a different code, follow the handling for that code rather than this playbook. For example, E-305 concerns a boiler that is not responding, while E-402 means mains power has been interrupted.

## Explain the safety response

Tell the customer that the thermostat has turned the heating off to be safe because its temperature sensor is disconnected. Make clear that the heating shutdown is the thermostat's response to this fault, not a setting the customer needs to change.

Do not promise that heating will resume before the fault is resolved. Do not recommend turning the heating back on through the app, changing the target temperature, starting a boost or changing the schedule as a way to overcome E-217. The fault's documented action is support arranging a replacement.

If asked why the shutdown occurs, explain only what is established: the temperature sensor is disconnected, and the thermostat turns the heating off to be safe. Do not speculate about the cause, repair method or expected time to resolution.

## Arrange a replacement through support

The customer should contact Dormouse support to arrange a replacement. Support can be contacted in the app under Help > Contact support.

Give the customer that route clearly. Do not direct them to attempt a thermostat repair or sensor reconnection as a substitute for contacting support. The documented action for E-217 is replacement arranged through Dormouse support.

Keep the support interaction focused on the reported code and the safe shutdown. Do not imply that the customer can resolve the fault by restarting the thermostat, pairing it again, changing Wi-Fi settings or replacing backup batteries. Those actions are not specified for E-217.

## Support handling and escalation

Support should record that E-217 was reported, that the customer was told the thermostat has turned the heating off to be safe, and that the customer was directed to Help > Contact support to arrange a replacement.

Use the internal support escalation levels where needed:

1. Level 1: app chat agents handle the initial report and provide the E-217 guidance.
2. Level 2: product specialists handle cases needing further product review.
3. Level 3: engineering handles technical investigation escalated by product specialists.

Escalation does not change the customer guidance for E-217: the thermostat has turned the heating off to be safe, and support arranges a replacement. Do not make a replacement commitment or give a timeline beyond the support process.

## Do not confuse E-217 with other faults

Use the error code, not a symptom alone, to identify the relevant handling. Several faults can affect heating or app information, but their documented responses differ.

| Code | Meaning | Relevant distinction |
|---|---|---|
| E-217 | Temperature sensor disconnected | Heating is turned off to be safe; contact support to arrange a replacement. |
| E-221 | Humidity sensor fault | Heating keeps working, but humidity readings disappear from the app. Contact support if the code stays for more than a day. |
| E-305 | Boiler not responding | Check the boiler is switched on, its pressure is between 1 and 1.5 bar, and its display for a fault. |
| E-402 | Mains power interrupted | The thermostat runs on backup batteries and cannot switch the heating on. |
| E-510 | Firmware update failed | The thermostat keeps its current firmware and tries again the next night. |

Do not apply another code's troubleshooting steps to E-217. In particular, E-221's continued heating operation does not apply to a temperature sensor fault.

## Customer communication checklist

Before closing or handing off the interaction, check that the customer has received the essential information:

- E-217 means the temperature sensor is disconnected.
- The thermostat turns the heating off to be safe.
- The customer should contact Dormouse support to arrange a replacement.
- The in-app route is Help > Contact support.

Use direct, calm wording. Avoid implying that the fault is harmless, that the heating is still available, or that a customer setting can override the safety response. If the code is not E-217, confirm the code and use the appropriate error-code guidance instead.

## QA and documentation notes

Review handling for accuracy against the E-217 guidance: the code means Temperature sensor disconnected; the thermostat turns the heating off to be safe; the customer should contact Dormouse support to arrange a replacement.

Check that support notes distinguish E-217 from E-221, where heating keeps working despite a humidity sensor fault. Also check that the response does not introduce unsupported troubleshooting steps, technical causes, repair instructions or resolution times.

Firmware releases are tested against the manual test-script library before rollout. For E-217 support material, QA should verify that the customer-facing description preserves the safe shutdown and replacement route, and does not contradict the error-code guidance.
