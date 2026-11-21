---
title: Radiator Valve Does Not Heat to Its Own Temperature
product: radiator valve
type: troubleshooting
audience: customer
firmware: 4.1
updated: 2026-01-13
---

# Radiator Valve Does Not Heat to Its Own Temperature

A Dormouse Radiator Valve can heat a radiator to its own temperature when it is part of a zone controlled by a Dormouse Thermostat. Work through the checks below in order.

## 1. Check the valve is in the intended zone

Each Dormouse Thermostat controls its own zone, with its own schedule. A Dormouse Radiator Valve must be joined to the zone whose heating you want it to control.

In the app or web dashboard, check which zone the valve belongs to. If it is in a different zone, it will follow that zone's control rather than the thermostat you expect. To add a valve to a zone, go to Settings > Home > Add a device.

A zone can include up to ten Dormouse Radiator Valves. Each valve in the zone can heat its radiator to its own temperature.

## 2. Check which thermostat controls the zone

Make sure the thermostat you are using controls the same zone as the valve. A home can have up to four Dormouse Thermostats, and each controls its own zone. A thermostat in another zone does not control this valve.

If you have several thermostats, check the zone assignments for both the valve and the thermostat in the app or web dashboard. The valve and any Room Sensor in a zone communicate with that zone's thermostat over a low-power radio link. Only the thermostat uses Wi-Fi.

## 3. Check the thermostat's status

Check the thermostat that controls the valve's zone. Its display shows the room temperature and target temperature. A flame symbol means the thermostat is asking the boiler for heat. If there is no heat request, the boiler may not be asked to heat the zone at that time.

You can change the target temperature by turning the thermostat's dial or using the app. A manual temperature change lasts until the next schedule period starts. A boost heats the home at the boost temperature for one hour; the display shows an upward arrow while it is running.

## 4. Check whether the boiler responds

If the thermostat is asking for heat but the radiator does not warm, check whether the boiler is responding to the heat request.

If the thermostat shows E-305, check that the boiler is switched on and that its pressure is between 1 and 1.5 bar. Then check the boiler's own display for a fault. If the thermostat shows E-312, the boiler has reported a fault of its own. Look up the fault in the boiler's manual, or call a registered gas engineer.

The thermostat may also show E-110 if it cannot reach the Dormouse cloud. In that case, it keeps running schedules, but changes made in the app wait until it reconnects. This code does not by itself indicate that the boiler has failed to respond.

## 5. Check for thermostat error codes

When the thermostat detects a problem, it shows an error code. The app shows the same code and can notify you about it.

- **E-217:** The temperature sensor is disconnected. The thermostat turns the heating off to be safe. Contact Dormouse support to arrange a replacement.
- **E-305:** The boiler is not responding. Check the boiler as described above.
- **E-312:** The boiler reports a fault. Refer to the boiler's manual or call a registered gas engineer.

For support, use Help > Contact support in the app.
