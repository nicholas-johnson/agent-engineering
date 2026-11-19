---
title: Understand when away mode changes through geofencing
product: app
type: support
audience: customer
firmware: 4.1
updated: 2025-06-19
---

# Understand when away mode changes through geofencing

Geofencing can turn away mode on and off automatically using the location of household members' phones. It uses whether members are near or away from home to decide when to change the mode.

## When away mode turns on

Away mode turns on when every household member who shares their location is more than 1 km from home. Members who do not share their location are not included in this check.

The change happens once all location-sharing members are beyond that distance.

## When away mode turns off

Away mode turns off when the first location-sharing member comes back within 1 km of home. Other members do not need to have returned.

## Choose who shares location

Each household member chooses whether to share their location in the app. Geofencing uses the choices made by members of the household.

Phone locations are never stored. Dormouse stores only whether each member is home or away.

## Stop geofencing for the home

To stop geofencing for the whole home, go to **Settings > Away > Geofencing**.

You can also turn away mode on in the app by tapping **Away**, or on the thermostat by choosing **Menu > Away**. Away mode keeps the home at the away temperature until it is turned off.
