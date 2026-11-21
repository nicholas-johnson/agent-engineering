---
title: Add Dormouse Devices to a Home Automation System
product: all
type: integration
audience: customer
firmware: 4.1
updated: 2026-09-01
---

# Add Dormouse Devices to a Home Automation System

Dormouse thermostats, room sensors and radiator valves are added to a Dormouse home through the Dormouse app or web dashboard. Add each device to the home and, where applicable, assign it to a zone before using it with a supported home automation system.

Dormouse devices do not all connect in the same way. A thermostat uses Wi-Fi to connect to your home network. Room sensors and radiator valves communicate with their zone's thermostat over a low-power radio link. Only the thermostat uses Wi-Fi.

## Check what your home supports

A home can have up to four Dormouse Thermostats. Each thermostat controls its own zone and has its own schedule. A Dormouse Room Sensor can join a zone to measure temperature and humidity in another room in that zone. Up to ten Dormouse Radiator Valves can join a zone, with each valve heating its radiator to its own temperature.

A room sensor measures temperature and humidity. It uses one CR2032 coin cell, which lasts about a year, and a zone can have up to three sensors.

A radiator valve fits M30 x 1.5 valve bodies. Adapters for other common valve types are included with the valve. It uses two AA batteries, which last about two years.

Check that the thermostat is already part of the Dormouse home before adding sensors or valves. You can then choose the zone each device should join.

## Prepare the thermostat

The thermostat must be wired to a compatible gas boiler by a qualified installer. It needs a 2.4 GHz Wi-Fi network; it cannot join a 5 GHz network. Pairing also requires the Dormouse app on a phone running Android 12 or later, or iOS 17 or later, and a Dormouse account.

If the thermostat has not been paired yet:

1. Hold the dial down for 5 seconds, until the display shows PAIR.
2. In the app, choose Add thermostat and follow the steps.
3. Keep your phone within 5 metres of the thermostat until the app says pairing has finished.

Pairing must finish within 3 minutes of PAIR appearing. If it does not, the display shows E-104. Hold the dial down for 5 seconds and start pairing again.

## Add a thermostat to the home

To add another thermostat to a home, open the Dormouse app or web dashboard and go to Settings > Home > Add a device. Follow the on-screen instructions to add the thermostat.

Each thermostat controls its own zone, with its own schedule. For example, one thermostat can control downstairs radiators and another can control upstairs radiators. Decide which area the new thermostat will control so that you can set up the right zone for it.

The app and web dashboard provide the home settings for adding devices. On the thermostat itself, Menu > Schedule shows today's periods, but schedules can only be changed in the app or web dashboard.

## Add a room sensor

Go to Settings > Home > Add a device in the Dormouse app or web dashboard, then follow the instructions to add the Dormouse Room Sensor. Select the zone it should join. The sensor measures temperature and humidity in another room of that zone and communicates with the zone's thermostat over a low-power 868 MHz radio link.

A sensor does not connect directly to Wi-Fi. Check that it is assigned to the intended zone, and bear in mind that each zone can have up to three Dormouse Room Sensors.

## Add a radiator valve

Go to Settings > Home > Add a device in the Dormouse app or web dashboard, then follow the instructions to add the Dormouse Radiator Valve. Choose the zone whose thermostat should communicate with it. The valve uses a low-power 868 MHz radio link to talk to that zone's thermostat; it does not connect directly to Wi-Fi.

Fit the valve to a compatible radiator valve body, using an included adapter if needed for another common valve type. Up to ten Dormouse Radiator Valves can join a zone. Each valve heats its own radiator to its own temperature.

## Confirm the device and zone

After adding a device, check the home's device list and confirm it is associated with the intended zone. A thermostat controls its own zone; a room sensor or radiator valve joins an existing zone and communicates with that zone's thermostat.

If a sensor or valve is assigned to the wrong zone, use Settings > Home > Add a device to review the home's devices and follow the available instructions. Do not try to join a sensor or valve to Wi-Fi: only the thermostat uses Wi-Fi.

## Connect supported devices to automations

Once the Dormouse devices are added to the home, follow the setup instructions provided by the home automation system to connect supported devices to its automations. The available connections and automation actions depend on that system. This guide does not specify which external systems or automation actions are supported.

Keep the distinction between the Dormouse home and the external automation setup clear: add and assign Dormouse devices in the Dormouse app or web dashboard first, then configure any supported automation in the other system.

## Maintain your devices

Keep thermostat firmware up to date. Firmware updates install automatically between 02:00 and 04:00 local time and cannot be postponed. During an update, the display shows UPDATING, the thermostat restarts, and heating pauses for about two minutes.

The thermostat's two backup AA batteries keep its clock and schedules during a power cut for up to 48 hours, but cannot switch the heating on while mains power is off. Replace them once a year, or when the display shows E-401. For help, use Help > Contact support in the Dormouse app.
