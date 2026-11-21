---
title: Radiator Valve Radio-Link Commissioning
product: radiator valve
type: installation
audience: customer
firmware: 4.1
updated: 2025-07-30
---

# Radiator Valve Radio-Link Commissioning

## Purpose and scope

This guide covers adding a fitted Dormouse Radiator Valve to a zone and checking that it communicates with the zone's Dormouse Thermostat over the low-power 868 MHz radio link.

A Dormouse Radiator Valve controls the temperature at its own radiator. It joins a zone that is controlled by a Dormouse Thermostat. The thermostat uses Wi-Fi; the valve communicates with its zone thermostat by radio and does not use Wi-Fi.

This guide assumes the valve has already been fitted to the radiator. Follow the valve's fitting instructions for mechanical installation. The thermostat must be installed and paired with the home before you add the valve.

## Equipment and compatibility

Check that the home has a Dormouse Thermostat for the zone you want to control. A home can have up to four thermostats, each controlling its own zone. A zone can include up to ten Dormouse Radiator Valves.

The Dormouse Radiator Valve fits M30 x 1.5 valve bodies. Adapters for other common valve types are supplied in the box. The valve runs on two AA batteries, which typically last about two years.

Valves and sensors communicate with their zone thermostat over a low-power 868 MHz radio link. Only the thermostat connects to Wi-Fi. If you are checking network connectivity, do not look for a Wi-Fi connection on the valve.

## Prepare the installation

Before adding the valve, identify the thermostat that controls the radiator's zone. Adding the valve to a different zone will associate it with the wrong thermostat.

Check that the thermostat is powered and working. Its display should show the room temperature and target temperature rather than an error code. If the thermostat displays an error, use the error-code guidance in the Dormouse Thermostat User Guide before continuing.

Make sure the valve has its two AA batteries installed. If the valve does not respond during commissioning, check the batteries and their orientation before repeating the add-device procedure.

## Add the valve to a zone

Use the Dormouse app or web dashboard to add a valve. The thermostat's on-device schedule view is not used for adding devices.

1. Open the app or web dashboard.
2. Go to Settings > Home > Add a device.
3. Choose the Dormouse Radiator Valve and follow the on-screen steps.
4. Select the thermostat and zone that control the radiator.
5. Complete the steps shown in the app or web dashboard.

The valve joins the selected zone and heats its radiator to its own temperature. Check the displayed device and zone details before finishing, especially in homes with more than one thermostat.

## Check the radio link

After adding the valve, check in the app or web dashboard that it appears in the intended zone and is available as a device in that zone. This confirms that the add-device process has completed.

For a practical check, make a small target-temperature change using the thermostat or app, then confirm that the valve responds as expected. The valve controls its own radiator temperature; the zone thermostat remains the controller for the zone.

If the valve does not appear or respond, check the following:

- Confirm that you added it to the correct zone and thermostat.
- Check that the thermostat is powered and not showing an error.
- Check that both AA batteries are correctly installed in the valve.
- Repeat Settings > Home > Add a device and follow the commissioning steps again.

The valve communicates with its zone thermostat over the 868 MHz radio link. Re-pairing the thermostat to Wi-Fi is not a radio-link check and is not required simply because a valve is being added.

## Completing the handover

Confirm that the valve is listed under the intended zone and that it responds to a temperature change. If the home has multiple thermostats, verify the other zones still show their expected devices and schedules.

Explain that the valve's batteries are replaceable and typically last about two years. The thermostat's backup batteries are separate: they keep its clock and schedules during a power cut, but the thermostat cannot switch the heating on while mains power is off.

For operating and schedule information, refer to the Dormouse Thermostat User Guide. For product help, contact Dormouse through Help > Contact support in the app.
