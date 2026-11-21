---
title: Away Mode Does Not Turn Off on Return
product: app
type: troubleshooting
audience: customer
firmware: 4.1
updated: 2025-07-18
---

# Away Mode Does Not Turn Off on Return

Away mode turns off when the first household member who shares their location comes back within 1 km of home. Use the checks below if away mode stays on after someone returns.

## Check that the member shares their location

Each household member chooses whether to share their location in the app. Geofencing uses the locations of members who share their location; a member who does not share theirs cannot trigger away mode to turn off.

Ask the returning member to check their location-sharing choice in the app. If they do not share their location, they can choose to enable it there.

## Check whether the member is within 1 km of home

Away mode turns off when the first member who shares their location comes back within 1 km of home. If the returning member is still more than 1 km away, away mode remains on.

Check whether the member has come back within that distance. Once a member who shares their location is within 1 km, geofencing should turn away mode off.

## Check whether geofencing is enabled for the home

Geofencing can be stopped for the whole home. In the app or web dashboard, go to **Settings > Away > Geofencing** and check that it is enabled.

If geofencing is stopped, it will not turn away mode off when a member returns. Enable it if you want the home to use members' shared locations to control away mode.

## Check the home's other members

Geofencing turns away mode on when every member who shares their location is more than 1 km from home. It turns away mode off when the first of those members comes back within 1 km.

A member who has not returned within 1 km does not prevent away mode from turning off once another sharing member is within range. Check that the returning person is a member of the home and shares their location.

## Turn away mode off manually

If you do not want to wait for geofencing, turn away mode off in the app, or on the thermostat choose **Menu > Away**. Away mode then stops keeping the home at its away temperature.
