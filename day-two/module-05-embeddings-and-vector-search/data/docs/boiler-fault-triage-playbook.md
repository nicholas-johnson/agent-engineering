---
title: Boiler Fault Triage Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-06-24
---

# Boiler Fault Triage Playbook

## Purpose and scope

Use this playbook to distinguish the two boiler-related errors shown by the Dormouse Thermostat:

- **E-305: Boiler not responding**
- **E-312: Boiler reports a fault**

Follow the documented checks and escalation guidance below. The thermostat display and the app show the same error code. Do not treat these codes as interchangeable: each indicates a different condition and has different next steps.

## Triage summary

| Code | What it means | First action |
|---|---|---|
| E-305 | The boiler is not responding to the thermostat. | Check that the boiler is switched on and that its pressure is between 1 and 1.5 bar. Then check the boiler's own display for a fault. |
| E-312 | The boiler has found a fault of its own. | Look up the fault in the boiler's manual, or call a registered gas engineer. |

Use the code displayed by the thermostat to select the corresponding procedure. For E-305, complete the checks in the order given. For E-312, use the boiler's own fault information and the documented escalation route.

## E-305: Boiler not responding

E-305 means the boiler is not responding. Carry out these checks:

1. Check that the boiler is switched on.
2. Check the boiler pressure. It should be between **1 and 1.5 bar**.
3. Check the boiler's own display for a fault.

If the boiler's display shows a fault, use the boiler's own manual to identify it and follow the guidance there. E-305 itself does not give the boiler's fault details; the thermostat's documented action is to check the boiler display after checking power and pressure.

Do not record E-305 as E-312 merely because the boiler display also shows a fault. Keep the thermostat code and any separate boiler-display information distinct when recording or handing over the case.

## E-312: Boiler reports a fault

E-312 means the boiler has found a fault of its own. The documented actions are:

1. Look up the fault in the boiler's manual; or
2. Call a registered gas engineer.

Use the boiler's own fault information for this triage. Do not apply the E-305 checklist as a substitute for identifying the boiler fault, and do not infer that E-312 means the boiler is switched off or that its pressure is outside the E-305 range. Those conditions are not what E-312 describes.

## Distinguishing the codes

Base the triage on the code shown by the thermostat:

- **E-305 describes a response problem:** the boiler is not responding. Check that it is switched on, check that pressure is between 1 and 1.5 bar, then inspect its display for a fault.
- **E-312 describes a boiler-reported fault:** consult the boiler's manual or call a registered gas engineer.

A boiler-display fault can be relevant during E-305 checks, but the thermostat code remains E-305 unless the thermostat displays E-312. Do not replace one code with the other in notes or customer guidance.

## Escalation guidance

For **E-305**, direct the user through the documented checks: boiler switched on, pressure between 1 and 1.5 bar, and boiler display checked for a fault. If the boiler display shows a fault, refer the user to the boiler's manual for that fault or to a registered gas engineer.

For **E-312**, the escalation guidance is explicit: the user should look up the boiler fault in the boiler's manual or call a registered gas engineer.

Do not give boiler repair instructions beyond these documented checks and routes. The thermostat guide does not specify further diagnostic steps or repairs for either code.

## Case notes and handover

Record the exact thermostat error code as displayed: **E-305** or **E-312**. For E-305, note whether the boiler is switched on, whether its pressure is within the stated range, and whether its own display shows a fault. If a boiler-display fault is reported, keep that information separate from the thermostat code.

For E-312, record that the boiler reports a fault and whether the user has been directed to the boiler's manual or to a registered gas engineer. Do not infer a boiler fault description that has not been provided by the user or identified from the boiler's own documentation.

## Limits of this playbook

This playbook covers the documented meaning, checks and escalation guidance for E-305 and E-312. It does not establish additional boiler diagnostics, repair procedures, or a guarantee that either check will resolve the issue. Follow the relevant boiler manual or registered gas engineer's guidance for boiler faults.
