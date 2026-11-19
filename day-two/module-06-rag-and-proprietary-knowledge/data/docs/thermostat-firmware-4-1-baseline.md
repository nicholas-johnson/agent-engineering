---
title: Thermostat Firmware 4.1 Baseline
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-04-07
---

# Thermostat Firmware 4.1 Baseline

## Purpose and scope

This internal baseline summarises the Dormouse Thermostat's firmware 4.1 behaviour and the user-visible functions support teams should expect. The user guide for firmware 4.1 is the source of truth for customer-facing behaviour. Use the notes here to set expectations and help identify when a reported behaviour differs from the documented product behaviour.

The thermostat works with the Dormouse app for Android and iOS, and with the web dashboard. Most settings can be changed in any of them. Menu paths in this document use the same format as the app and web dashboard.

The thermostat is mains-powered through its wall plate. Its two AA backup batteries preserve the clock and schedules during a power cut for up to 48 hours; they do not allow it to switch on the heating while mains power is off.

## Firmware identification

The thermostat's firmware version appears under Menu > About. The menu opens when the display shows the room temperature and the user presses the dial. Turn the dial to move between Schedule, Away, Settings and About, then press to select.

The thermostat display shows room temperature prominently and the target temperature underneath. Turning the dial enlarges the target temperature while it is being changed. After 20 seconds without a touch, the display dims. Users turn the dial to change the target temperature and press to confirm.

Firmware 4.1 is the current documented firmware baseline. Support should distinguish a firmware version from a hardware revision: the hardware revisions are A, B and C, and serial numbers begin DMA, DMB or DMC respectively. The hardware revision is not the firmware version.

## Temperature control and heating

The target temperature is adjustable from 5 to 30 degrees in half-degree steps. A change made by hand lasts until the next schedule period starts. Users can adjust the target using the dial or the app.

A boost heats the home at the boost temperature for one hour. The display shows an upward arrow while the boost is running. Pressing the boost button again cancels it. The default boost temperature is 21 degrees; users can change it in Settings > Heating > Boost temperature.

Frost protection is always on and cannot be disabled. If the room temperature falls below 5 degrees, the thermostat turns on the heating, including when heating is off or away mode is on. The display shows a snowflake while frost protection is heating.

The flame symbol means the thermostat is asking the boiler for heat. A sunrise symbol means Warm Wake is heating ahead of the next schedule period. Support may identify the symbol, but must not describe how Warm Wake works, how early it starts, or where its setting is.

## Schedules and away mode

Each day can have up to six schedule periods. A period has a start time and target temperature, and lasts until the next period starts. Users edit schedules in the Schedule tab of the app or web dashboard. On the thermostat, Menu > Schedule displays today's periods but does not allow edits. Copy day applies the same periods to other days.

Away mode holds the home at the away temperature until it is turned off. The default is 16 degrees; users can change it in Settings > Away > Away temperature. It can be turned on in the app or under Menu > Away on the thermostat.

Geofencing uses the location of household members' phones. Away mode turns on when every member who shares their location is more than 1 km from home; it turns off when the first of them comes back within 1 km. Each member controls location sharing in the app. Geofencing for the whole home can be stopped in Settings > Away > Geofencing.

## Devices, zones and household access

A home can have up to four Dormouse Thermostats, each controlling its own zone and schedule. A Dormouse Room Sensor can join a zone to measure temperature in another room. Up to ten Dormouse Radiator Valves can join a zone, with each valve controlling its radiator's temperature. Add a thermostat, sensor or valve through Settings > Home > Add a device.

Valves and sensors communicate with their zone's thermostat over a low-power 868 MHz radio link. Only the thermostat uses Wi-Fi. A thermostat requires a 2.4 GHz Wi-Fi network; it cannot join a 5 GHz network.

A home has one owner and up to eight members. Members can change temperature, schedules and away mode. Only the owner can add or remove devices, invite members or remove members. Invitations are sent through Settings > Household > Invite and work for 7 days.

## Accounts, reports and notifications

Users sign in to the app and web dashboard with an email address and password. Passwords must contain at least 10 characters. Two-step verification can be enabled in Settings > Account > Two-step verification. On a new phone or browser, sign-in also requires a 6-digit code, sent by email or supplied by an authenticator app if configured.

Password reset links work for 30 minutes and can be used once. If a link expires, the user needs to request another from Forgot password? on the sign-in screen.

An energy report arrives on the 1st of each month in the app's Energy tab. It shows daily heating hours compared with the previous month and estimated gas use in kWh. The estimate depends on boiler size, entered under Settings > Home > Boiler size. Heating history is kept for 2 years.

Users choose their own notifications in Settings > Notifications. Available notifications cover thermostat error codes, low backup batteries, heating on for 2 hours while everyone is away, installed firmware updates and monthly energy reports. Phone locations are not stored; the system stores only whether each member is home or away.

## Connectivity, power and error handling

Pairing connects the thermostat to Wi-Fi and the user's account. The user holds the dial for 5 seconds until PAIR appears, then follows Add thermostat in the app. Pairing must finish within 3 minutes, with the phone within 5 metres of the thermostat. If it times out, the display shows E-104 and pairing must be started again.

For E-101, check that the router is on and provides a 2.4 GHz network. If the network name or password has changed, pair the thermostat again. For E-110, check the router's internet connection. The thermostat continues to run schedules while it cannot reach the Dormouse cloud; app changes wait until it reconnects.

E-402 means mains power is interrupted. The thermostat preserves the clock and schedules on backup batteries for up to 48 hours but cannot switch on the heating. E-401 means backup batteries are low; replace the two AA batteries behind the front cover within a month. The guide also recommends replacing them yearly.

For boiler issues, E-305 means the boiler is not responding: check it is on, its pressure is between 1 and 1.5 bar, and its own display for a fault. E-312 means the boiler reports a fault; refer to the boiler manual or contact a registered gas engineer. For E-217, the heating is turned off to be safe and Dormouse support should arrange a replacement. For E-221, heating continues but humidity readings disappear; contact support if it remains for more than a day.

## Firmware updates and release history

Firmware updates install automatically between 02:00 and 04:00 local time and cannot be postponed. During installation, the display shows UPDATING and the thermostat restarts. Installation takes about two minutes, and heating pauses until it finishes.

If an update fails, the display shows E-510. The thermostat keeps its current firmware and retries the next night. There is no user action required.

Relevant release history:

| Version | Date | Notable user-visible change |
|---|---|---|
| 3.0 | 2025-01-20 | Two-step verification; support for four thermostats per home. |
| 3.1 | 2025-03-17 | Geofencing; adjustable away temperature. |
| 3.2 | 2025-05-26 | Monthly energy reports; E-110 for cloud connectivity loss. |
| 3.3 | 2025-08-11 | Support for eight household members; invitations expire after 7 days. |
| 3.4 | 2025-10-06 | Radiator Valve support; update window changed to 02:00-04:00. |
| 3.5 | 2025-12-01 | E-510 retries the next night; E-401 appears a month before batteries run out. |
| 4.0 | 2026-03-09 | Warm Wake, new display symbols and Room Sensor support. |
| 4.1 | 2026-08-17 | Adjustable boost temperature; password reset links work for 30 minutes. |

## Support and internal rollout notes

For help with a reported issue, direct users to Help > Contact support in the app. Before escalating, record the displayed error code, firmware version from Menu > About, and whether the issue affects thermostat controls, app changes or a connected device. Follow the user guide's action for the relevant error code; do not infer a fault from a symbol alone.

Internally, support has three levels: Level 1 app chat agents, Level 2 product specialists and Level 3 engineering. Firmware rollout proceeds to 1% of thermostats, then 10%, then every thermostat over a week. Every release is tested against the manual test-script library before rollout.

A factory reset removes Wi-Fi details, schedules and the account link. It is intended before giving the thermostat to someone else or moving house without it. Hold the dial and boost button together for 10 seconds until RESET appears; the thermostat restarts ready to pair again.
