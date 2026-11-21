---
title: New Device Addition and Commissioning Checklist
product: all
type: installation
audience: customer
firmware: 4.1
updated: 2026-10-18
---

# New Device Addition and Commissioning Checklist

Use this checklist to add and commission a Dormouse Thermostat, Dormouse Radiator Valve or Dormouse Room Sensor. A home can have up to four thermostats. Each thermostat controls its own zone, with its own schedule. A zone can include one Room Sensor and up to ten Radiator Valves.

## 1. Confirm the installation

Before adding a device, identify the zone it will serve and confirm that the home has capacity for it.

- Each thermostat controls a separate zone.
- A Room Sensor measures temperature and humidity in another room of its zone.
- Radiator Valves allow each radiator in a zone to heat to its own temperature.
- Valves and sensors communicate with the thermostat for their zone over a low-power 868 MHz radio link. They do not use Wi-Fi; only the thermostat uses Wi-Fi.
- Use the Dormouse app or web dashboard to manage devices. Most settings are available in either.

If the device is a thermostat, confirm that it is intended for indoor use between 0 and 40 degrees. It is 84 mm across and 24 mm deep, with a mains-powered wall plate. Thermostat wiring to the boiler must be carried out by a qualified installer.

## 2. Check power and device requirements

Check the device's power arrangements before starting commissioning.

| Device | Power and relevant requirements |
|---|---|
| Dormouse Thermostat | Powered by mains through its wall plate. It requires a 2.4 GHz Wi-Fi network; it cannot join a 5 GHz network. |
| Dormouse Radiator Valve | Runs on two AA batteries, which last about two years. It fits M30 x 1.5 valve bodies; adapters for other common valves are supplied in the box. |
| Dormouse Room Sensor | Runs on one CR2032 coin cell, which lasts about a year. Up to three sensors can join a zone. |

A thermostat also requires the Dormouse app on Android 12 or later, or iOS 17 or later, and a Dormouse account. Keep the app available during setup.

## 3. Prepare the thermostat

If installing a thermostat, make sure it is wired to the boiler by a qualified installer and that mains power is available. Pairing connects the thermostat to Wi-Fi and to the Dormouse account.

For a thermostat that needs pairing:

1. Hold the dial down for 5 seconds, until the display shows PAIR.
2. In the app, choose Add thermostat and follow the steps.
3. Keep the phone within 5 metres of the thermostat until the app confirms completion.

Pairing must finish within 3 minutes of PAIR appearing. If it does not, E-104 appears and pairing must be started again. A thermostat needs a 2.4 GHz Wi-Fi network, not a 5 GHz network.

## 4. Start adding the device

In the app or web dashboard, go to Settings > Home > Add a device. Select the device type and follow the displayed instructions.

For a thermostat, complete the pairing process in the app. Keep the phone close to the thermostat until the app reports that setup has finished.

For a Radiator Valve or Room Sensor, follow the app or dashboard instructions to add it to the intended zone. Confirm that the selected zone is controlled by the thermostat with which the device needs to communicate.

## 5. Fit the device

Fit each device according to its intended use and the on-screen commissioning instructions.

For a Radiator Valve, check the radiator valve body before fitting. The valve fits M30 x 1.5 bodies. Use an adapter from the box for other common valve types where required. Confirm the valve is assigned to the zone whose radiator it controls.

For a Room Sensor, place it in the room where the zone's temperature and humidity are to be measured. Confirm it is assigned to the correct zone. A zone supports up to three Room Sensors.

Do not treat a Radiator Valve or Room Sensor as a Wi-Fi device. Both communicate with their zone thermostat over the low-power 868 MHz radio link.

## 6. Verify registration and zone assignment

After adding the device, check the home's device list and confirm that the new device appears. Verify its assigned zone before leaving commissioning.

- Confirm that a thermostat is listed for the intended zone. A home supports up to four thermostats.
- Confirm that each Radiator Valve is assigned to the zone it serves. A zone supports up to ten valves.
- Confirm that each Room Sensor is assigned to the intended zone. A zone supports up to three sensors.
- Check that no device has been added to a different zone by mistake.

A thermostat's menu can show schedule information, but schedule periods are changed in the app or web dashboard.

## 7. Check operation and display indications

Check the thermostat display and app for any reported errors. The display shows room temperature and target temperature. A Wi-Fi symbol with a cross indicates that the thermostat is not connected to Wi-Fi. The app shows the same error code as the thermostat and can notify members about errors.

Use the error code to decide what action is needed:

| Code | Commissioning action |
|---|---|
| E-101 | Check that the router is on and provides a 2.4 GHz network. If the network name or password changed, pair the thermostat again. |
| E-104 | Start pairing again by holding the dial for 5 seconds. Keep the phone within 5 metres and finish within 3 minutes. |
| E-110 | Check that the router is connected to the internet. The thermostat continues running schedules; app changes wait until it reconnects. |
| E-217 | The thermostat turns heating off to be safe. Contact Dormouse support to arrange a replacement. |
| E-305 | Check that the boiler is on and pressure is between 1 and 1.5 bar. Check the boiler display for a fault. |
| E-312 | Consult the boiler manual or contact a registered gas engineer. |

Contact support in the app under Help > Contact support.

## 8. Complete handover

Before handover, confirm that the device is visible in the app or web dashboard, assigned to the correct zone, and free of unresolved commissioning errors. Explain that thermostat schedules are managed in the app or dashboard, and that members can change temperatures, schedules and away mode.

A thermostat has two AA backup batteries behind its front cover. They keep the clock and schedules during a power cut for up to 48 hours, but cannot switch on the heating while mains power is off. Replace them once a year, or within a month of E-401 appearing.

The thermostat installs firmware updates automatically between 02:00 and 04:00 local time. During an update, heating pauses for about two minutes. If E-510 appears, the thermostat keeps its current firmware and tries again the next night.
