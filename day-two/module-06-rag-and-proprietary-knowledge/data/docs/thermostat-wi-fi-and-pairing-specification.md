---
title: Thermostat Wi-Fi and Pairing Specification
product: thermostat
type: specification
audience: customer
firmware: 4.1
updated: 2025-09-25
---

# Thermostat Wi-Fi and Pairing Specification

## Product scope

This specification covers the Dormouse Thermostat's Wi-Fi requirements and its pairing process. Pairing connects the thermostat to a Wi-Fi network and to a Dormouse account.

The thermostat works with the Dormouse app for Android and iOS and with the web dashboard. Pairing is started in the app.

To check the thermostat's firmware version, press the dial to open the menu, then choose Menu > About. This specification applies to firmware 4.1.

## Wi-Fi requirements

The thermostat requires a Wi-Fi network that operates on 2.4 GHz. It cannot join a 5 GHz network.

Before pairing, check that the router is switched on and that the network offers 2.4 GHz Wi-Fi. If the thermostat cannot find the network, it displays E-101. Check the router and network configuration before trying again.

If the Wi-Fi network's name or password has changed, pair the thermostat again using the updated network details.

## Account and phone requirements

Pairing requires a Dormouse account and the Dormouse app on a phone running Android 12 or later, or iOS 17 or later. Create an account in the app if needed.

Keep the phone within 5 metres of the thermostat for the duration of pairing. The app indicates when pairing has finished; do not treat the process as complete until it does.

## Starting pairing

1. On the thermostat, hold the dial down for 5 seconds, until the display shows PAIR.
2. In the Dormouse app, choose Add thermostat and follow the steps.
3. Keep the phone within 5 metres of the thermostat until the app says pairing has finished.

The thermostat must finish pairing within 3 minutes of showing PAIR. If the process takes longer, the display shows E-104 and pairing must be started again.

## Pairing timeout and recovery

E-104 means pairing timed out. To retry, hold the dial down for 5 seconds to show PAIR, then start again in the app. Keep the phone within 5 metres and complete the app steps within 3 minutes.

Starting pairing again begins a new 3-minute window. If pairing times out again, check that the phone remains close to the thermostat and that the required 2.4 GHz network is available.

## Wi-Fi connection errors

E-101 indicates that the Wi-Fi network was not found. Check that the router is on and offers a 2.4 GHz network. If the network name or password has changed, pair the thermostat again.

E-110 indicates that the thermostat cannot reach the Dormouse cloud. Check that the router is connected to the internet. The thermostat continues to run its schedules while disconnected; changes made in the app wait until it reconnects.

The Wi-Fi symbol with a cross on the display indicates that the thermostat is not connected to Wi-Fi.

## Related connectivity information

The Dormouse Radiator Valve and Dormouse Room Sensor communicate with their zone's thermostat over a low-power 868 MHz radio link. They do not use Wi-Fi to connect to the home network; only the thermostat uses Wi-Fi.

Pairing connects the thermostat to Wi-Fi and to the Dormouse account. It is distinct from adding a device to a zone, which is done in Settings > Home > Add a device.

## Document scope and support

This specification describes the supported Wi-Fi band, prerequisites, pairing steps and recovery for pairing and connection errors. It does not specify router setup procedures beyond the checks described above.

For assistance, contact Dormouse support in the app under Help > Contact support.
