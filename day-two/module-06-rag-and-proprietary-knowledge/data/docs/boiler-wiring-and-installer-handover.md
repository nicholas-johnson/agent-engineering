---
title: Boiler Wiring and Installer Handover
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-01-18
---

# Boiler Wiring and Installer Handover

## Purpose and scope

This document sets out the requirements for wiring a Dormouse Thermostat to a supported gas boiler and the checks to complete at handover. It is for qualified installers. The thermostat supports combi, system and conventional gas boilers; it must be wired to the boiler by a qualified installer.

Use the boiler manufacturer's installation instructions and applicable local requirements when carrying out the work. This document does not provide terminal assignments, wiring diagrams, electrical ratings or boiler-specific procedures. Confirm those details from the relevant equipment documentation before making connections.

The thermostat controls one zone. A home can have up to four Dormouse Thermostats, each with its own zone and schedule. A Dormouse Room Sensor or Dormouse Radiator Valves can be added to a zone, but these devices do not replace the wired thermostat-to-boiler connection.

## Equipment and site requirements

Before installation, confirm the following:

- The boiler is a gas combi, system or conventional boiler.
- A qualified installer is available to make and verify the boiler wiring.
- The installation has a suitable mains supply for the thermostat wall plate.
- A 2.4 GHz Wi-Fi network is available for pairing. The thermostat cannot join a 5 GHz network.
- The customer has access to the Dormouse app on a phone running Android 12 or later, or iOS 17 or later, and has or can create a Dormouse account.

The thermostat is powered by mains through its wall plate. Its two AA backup batteries keep the clock and schedules during a power cut for up to 48 hours; they do not let the thermostat switch the heating on while mains power is off. The batteries should be replaced yearly or when E-401 appears.

Dormouse Radiator Valves and Room Sensors communicate with their zone's thermostat over a low-power 868 MHz radio link. Only the thermostat uses Wi-Fi.

## Wiring requirements and limits

Wire the thermostat to the boiler using the equipment documentation and the site-specific installation design. Verify that the selected boiler and connection method are supported before proceeding. Do not infer terminal functions, voltages or switching arrangements from this document.

After wiring, confirm that the thermostat has mains power and that the boiler responds to a heating demand. The thermostat's flame symbol means it is asking the boiler for heat; it does not by itself confirm that the boiler has produced heat. Check the boiler directly as part of commissioning.

The thermostat's response to certain faults is relevant to the handover:

- If the boiler is not responding, E-305 is shown. Check that the boiler is switched on and its pressure is between 1 and 1.5 bar, then check the boiler's own display for a fault.
- If the boiler reports a fault, E-312 is shown. Refer to the boiler's manual or have a registered gas engineer investigate.
- If the thermostat temperature sensor disconnects, E-217 is shown and the thermostat turns the heating off to be safe. Contact Dormouse support to arrange a replacement.

Do not leave a known boiler fault or an unverified heating response as a completed handover.

## Commissioning and functional checks

Complete the following checks after wiring, using the relevant boiler documentation for any boiler-specific steps:

1. **Check the installation.** Confirm that the thermostat is securely installed on its wall plate and that the boiler and thermostat supplies are in their intended operating state.
2. **Check temperature control.** Turn the dial to set a target temperature, then press it to confirm. The target can be set from 5 to 30 degrees in half-degree steps. A manual change lasts until the next schedule period starts.
3. **Check a heating demand.** Request heat using the thermostat or app. Confirm that the display shows the flame symbol when the thermostat is asking the boiler for heat, and verify the boiler's response at the boiler.
4. **Check the boiler status.** Look at the boiler's own display for faults. If E-305 or E-312 appears, follow the guidance in the error-code section of this document and resolve the issue before handover.
5. **Check the connection.** Pair the thermostat through the app and confirm that it connects to the household Wi-Fi and Dormouse account. The network must be 2.4 GHz. Keep the phone within 5 metres while pairing; pairing must finish within 3 minutes of PAIR appearing on the display.

Record any failed check, corrective action and outcome. Do not treat a successful app connection as proof that boiler wiring or boiler operation has been verified.

## Pairing and customer setup

Pairing connects the thermostat to Wi-Fi and the customer's Dormouse account. To start pairing, hold the dial down for 5 seconds until PAIR appears. In the app, choose Add thermostat and follow the steps. Keep the phone within 5 metres of the thermostat until the app confirms completion.

If pairing takes longer than 3 minutes, E-104 appears. Start again by holding the dial for 5 seconds and repeat the process. If the Wi-Fi network cannot be found, E-101 appears; check that the router is on and offers a 2.4 GHz network.

Show the customer how to open the menu by pressing the dial when the display shows the room temperature. The menu contains Schedule, Away, Settings and About. Menu > Schedule shows today's periods, but schedules can only be changed in the app or web dashboard.

## Handover checks to record

Record the following information in the installation handover record:

| Check | Record |
|---|---|
| Site and zone | Identify the thermostat's zone and the area it controls. |
| Boiler type | Combi, system or conventional gas boiler. |
| Installer verification | Confirm that a qualified installer completed the wiring and checked it against the relevant equipment documentation. |
| Mains and display | Confirm mains power is present and the thermostat display operates. |
| Heating demand | Record whether the boiler responded to a thermostat demand and whether any error code appeared. |
| Boiler status | Record whether the boiler display showed a fault and any action taken. |
| Pairing | Record whether pairing completed, including any error code or retry. |
| Customer handover | Confirm that the customer knows how to change the target temperature and where to find the Schedule and Away controls. |
| Open issues | Record outstanding checks, faults, corrective actions and who will follow them up. |

Include relevant observations, not assumptions. In particular, record the result of the heating-demand test separately from the thermostat's flame symbol.

## Faults, escalation and support

Use the thermostat's displayed code and the boiler's own indicators to identify the next action. E-305 means the boiler is not responding: check that it is switched on, verify pressure is between 1 and 1.5 bar, and inspect the boiler display for a fault. E-312 means the boiler reports a fault: consult the boiler manual or arrange investigation by a registered gas engineer.

For E-217, the thermostat turns heating off to be safe; contact Dormouse support to arrange a replacement. For E-101, verify the router and 2.4 GHz network. For E-104, restart pairing and complete it within 3 minutes, keeping the phone within 5 metres.

Dormouse support is available in the app under Help > Contact support. Include the thermostat error code, the checks already completed and the handover observations. Do not report a boiler fault as resolved unless the boiler has been checked and the result recorded.

## Internal support and QA notes

Support has three levels: level 1 app chat agents, level 2 product specialists and level 3 engineering. Escalate according to the support process when the reported issue cannot be resolved at the current level. Provide the error code, thermostat and boiler observations, and the checks already performed.

Every firmware release is tested against the manual test-script library before rollout. Firmware is rolled out to 1%, then 10%, then every thermostat over a week. These rollout details are internal and are not part of the customer handover.

The current firmware is 4.1. To check the installed version, press the dial to open the menu and choose Menu > About. Updates install automatically between 02:00 and 04:00 local time; during installation, heating pauses for about two minutes. If an update fails, E-510 appears and the thermostat tries again the next night.
