---
title: Thermostat Wi-Fi Setup After Installation
product: thermostat
type: installation
audience: customer
firmware: 4.1
updated: 2026-03-22
---

# Thermostat Wi-Fi Setup After Installation

## Purpose and scope

This guide explains how to connect an installed Dormouse Thermostat to a 2.4 GHz Wi-Fi network and a Dormouse account. Pairing is required to bring the thermostat online.

The thermostat must already be wired to a compatible gas boiler by a qualified installer. It works with combi, system and conventional gas boilers. Do not use this guide to install or wire the thermostat.

The thermostat connects to Wi-Fi. Dormouse Radiator Valves and Dormouse Room Sensors communicate with their zone's thermostat over a low-power 868 MHz radio link and do not connect directly to Wi-Fi.

## Network and account requirements

Before you begin, check the following:

- Your Wi-Fi network is on 2.4 GHz. The thermostat cannot join a 5 GHz network.
- The router is switched on and the network is available.
- You have a Dormouse account. Create one in the Dormouse app if needed.
- The Dormouse app is installed on a phone running Android 12 or later, or iOS 17 or later.
- The phone can stay within 5 metres of the thermostat until pairing finishes.

Pairing connects the thermostat to both the Wi-Fi network and your Dormouse account. Have the network details ready in the app when you start. If the network name or password changes later, pair the thermostat again.

## Check the thermostat before pairing

Confirm that the thermostat has mains power and that its display is on. The thermostat is powered through its wall plate; its backup batteries do not enable it to switch the heating on while mains power is off.

To check the firmware version, press the dial to open the menu, then choose Menu > About. This guide covers firmware 4.1.

If the thermostat is showing an error code, check the error code table in the user guide before proceeding. In particular, E-402 means mains power is interrupted: the thermostat can keep its clock and schedules on backup batteries for up to 48 hours, but cannot switch the heating on.

## Start pairing

Pairing must finish within 3 minutes of the thermostat showing PAIR. Keep the phone within 5 metres of the thermostat throughout the process.

1. Hold the thermostat dial down for 5 seconds.
2. Release it when the display shows PAIR.
3. In the Dormouse app, choose Add thermostat.
4. Follow the app's steps to connect the thermostat to Wi-Fi and your Dormouse account.
5. Wait for the app to confirm that pairing has finished.

Do not leave the phone out of range while the app is completing setup. If pairing takes longer than 3 minutes, the display shows E-104. Start again by holding the dial down for 5 seconds.

## Confirm the connection

When the app says setup is complete, the thermostat has been paired with the network and account. Check that the thermostat is not showing the Wi-Fi symbol with a cross. That symbol means it is not connected to Wi-Fi.

You can use the Dormouse app or web dashboard to change most settings. Menu paths in the app and web dashboard are the same. The thermostat continues to run its schedules if it cannot reach the Dormouse cloud, but changes made in the app wait until the connection is restored.

## Troubleshooting Wi-Fi and pairing

| Display or problem | What to do |
|---|---|
| E-101: Wi-Fi network not found | Check that the router is on and offers a 2.4 GHz network. If the network name or password has changed, pair the thermostat again. |
| E-104: Pairing timed out | Hold the dial down for 5 seconds to show PAIR and start again. Keep the phone within 5 metres, and finish within 3 minutes. |
| E-110: Cannot reach the Dormouse cloud | Check that the router is connected to the internet. The thermostat keeps running its schedules. App changes wait until it reconnects. |
| Wi-Fi symbol with a cross | The thermostat is not connected to Wi-Fi. Check the router and network, then pair again if required. |

If the thermostat continues to show an error, contact Dormouse support in the app under Help > Contact support. Include the displayed error code when you contact support.

## After setup

Once online, the thermostat can be managed using the Dormouse app or web dashboard. Members of a household can change the temperature, schedules and away mode. Only the home owner can add or remove devices, invite members or remove them.

Pairing does not change the heating schedule. On the thermostat, Menu > Schedule shows today's periods; schedule changes are made in the app or web dashboard.

If the thermostat is being transferred to someone else or moved house without it, use a factory reset first. Hold the dial and boost button down together for 10 seconds, until the display shows RESET. This removes the Wi-Fi details, schedules and link to the account. The thermostat then restarts and can be paired again.
