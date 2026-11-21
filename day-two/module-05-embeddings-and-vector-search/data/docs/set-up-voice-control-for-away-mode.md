---
title: Set Up Voice Control for Away Mode
product: app
type: integration
audience: customer
firmware: 4.1
updated: 2026-09-20
---

# Set Up Voice Control for Away Mode

## What you can do

A connected voice assistant may be able to turn Dormouse away mode on or off. The available controls depend on the assistant and its Dormouse integration. This guide explains how to make away mode available; it does not guarantee that every integration supports both commands.

Away mode keeps the home at the away temperature until you turn it off. The temperature is 16 degrees unless you change it in Settings > Away > Away temperature.

## What you need

Before you begin, make sure:

- Your Dormouse Thermostat is paired with your Wi-Fi network and Dormouse account.
- You can sign in to the Dormouse app or web dashboard.
- Your voice assistant supports a Dormouse integration and the away mode controls you want to use.
- You have access to the account or home-automation settings needed to connect the integration.

The thermostat requires a 2.4 GHz Wi-Fi network. Connected devices such as room sensors and radiator valves communicate with their zone's thermostat over a low-power radio link; only the thermostat uses Wi-Fi.

## Connect the integration

Use the setup instructions supplied by your voice assistant or home-automation system to connect Dormouse. Sign in with your Dormouse account when prompted and select the home that contains the thermostat.

The exact steps and available controls depend on the integration. Check its setup information for whether it can turn away mode on, turn it off, or both. If Dormouse is not offered as a supported service, you cannot enable this control through that integration.

## Enable away mode control

After connecting Dormouse, open the integration's device or service controls and check whether away mode is available for your home. Follow the integration's instructions to enable or expose that control.

Some integrations may show away mode as a switch or as a supported voice command. Others may not provide an away mode control. Dormouse does not define the names of controls or voice commands in another system.

## Use away mode

If your integration supports the control, use its available command or control to turn away mode on or off. You can also turn it on in the Dormouse app, or on the thermostat by choosing Menu > Away.

Away mode remains on until it is turned off. Changing the away temperature in Settings > Away > Away temperature changes the temperature used by away mode, including when you turn it on through a connected integration.

Frost protection remains active while away mode is on. If the room falls below 5 degrees, the thermostat turns the heating on to protect the pipes.

## Geofencing and voice control

Geofencing can also turn away mode on or off, using the location of household members' phones. Away mode turns on when every member who shares their location is more than 1 km from home, and turns off when the first of them comes back within 1 km.

Each member chooses whether to share their location in the app. To stop geofencing for the whole home, go to Settings > Away > Geofencing. Geofencing and a connected voice assistant are separate ways to control away mode.

## Check the connection

If away mode does not appear in the connected system:

1. Check that the Dormouse Thermostat is connected to Wi-Fi.
2. Confirm that the integration is connected to the Dormouse account and the correct home.
3. Check the integration's instructions to confirm that it supports away mode control.
4. If the thermostat shows an error code, check the code in the app or in the Error codes section of the Dormouse Thermostat User Guide.

When the thermostat cannot reach the Dormouse cloud, it keeps running its schedules, but changes made in the app wait until it reconnects. An integration may also be unable to send changes while the connection is unavailable.

## Control away mode without an integration

You can turn away mode on in the Dormouse app by tapping Away, or on the thermostat by choosing Menu > Away. These controls remain available whether or not you connect a voice assistant.
