---
title: App Changes Wait While the Thermostat Is Offline
product: app
type: troubleshooting
audience: customer
firmware: 4.1
updated: 2025-05-26
---

# App Changes Wait While the Thermostat Is Offline

## What this means

If a change you make in the Dormouse app does not appear on your thermostat, the thermostat may be unable to reach the Dormouse cloud. The cloud is the service that lets the app and thermostat exchange changes.

The thermostat keeps running its schedules while it cannot reach the cloud. Changes made in the app wait until the thermostat reconnects. They are not applied while it is offline.

## Check the thermostat display

Look at the thermostat for a Wi-Fi symbol with a cross. This means the thermostat is not connected to Wi-Fi.

The display may also show an error code:

- **E-101** means the thermostat cannot find the Wi-Fi network.
- **E-110** means the thermostat cannot reach the Dormouse cloud.

The app shows the same error code as the thermostat and can notify you about it.

## Check the Wi-Fi network

The thermostat needs a 2.4 GHz Wi-Fi network. It cannot join a 5 GHz network.

Check that your router is switched on and offers a 2.4 GHz network. If the display shows E-101, make sure the network is available to the thermostat.

If you have changed the Wi-Fi network name or password, pair the thermostat again:

1. Hold the dial down for 5 seconds, until the display shows PAIR.
2. In the app, choose Add thermostat and follow the steps.
3. Keep your phone within 5 metres of the thermostat until the app says pairing has finished.

Pairing must finish within 3 minutes of the display showing PAIR. If it takes longer, the thermostat shows E-104. Start pairing again.

## Check the internet connection

If the thermostat is connected to Wi-Fi but shows E-110, check that your router is connected to the internet.

E-110 means the thermostat cannot reach the Dormouse cloud. It does not mean the thermostat has stopped running your schedules: those continue while it is offline.

## Allow time for reconnection

Once the Wi-Fi and internet connections are available again, the thermostat can reconnect to the Dormouse cloud. App changes that were waiting are applied after it reconnects.

Check the thermostat display and app for the error code. If E-110 remains, check the router's internet connection again. For help with an error, contact Dormouse support in the app under Help > Contact support.
