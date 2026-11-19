---
title: Cloud Reachability Support Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-06-28
---

# Cloud Reachability Support Playbook

## Purpose and scope

Use this playbook when a Dormouse Thermostat shows E-110 or a member reports that app changes are not taking effect. E-110 means the thermostat cannot reach the Dormouse cloud.

The thermostat can remain connected to Wi-Fi while it cannot reach the cloud. The Wi-Fi symbol with a cross means the thermostat is not connected to Wi-Fi; E-110 indicates that the cloud cannot be reached. Do not treat these as interchangeable symptoms.

This playbook covers symptom checks, router internet checks, what continues to work while the thermostat is disconnected, and what to do about app changes that are waiting to take effect. It applies to the Dormouse Thermostat with firmware 4.1.

## Symptoms and impact

The thermostat display shows E-110. The app shows the same code and may notify the member about it. While cloud access is unavailable, the thermostat keeps running its schedules. Changes made in the app wait until the thermostat reconnects.

E-110 does not, by itself, mean that the thermostat has lost its schedules or stopped following them. It means the thermostat cannot reach the Dormouse cloud. Explain this distinction before asking the member to change settings or start pairing again.

Check what the member is seeing:

- E-110 on the thermostat or in the app: investigate internet access to the cloud.
- Wi-Fi symbol with a cross: investigate the thermostat's Wi-Fi connection. If the network name or password has changed, the thermostat may need to be paired again.
- App changes waiting to take effect: explain that they wait until the thermostat reconnects.

Do not promise that app changes will apply at a particular time. Their delivery depends on the thermostat reconnecting.

## Information to collect

Record the thermostat's displayed code, whether the app shows the same code, and whether the thermostat shows a Wi-Fi symbol with a cross. Ask when the issue began and whether the member knows of a router outage or a change to the Wi-Fi network name or password.

Confirm whether the thermostat is still running the schedule as expected. This helps distinguish a cloud reachability issue from a heating or boiler fault. If the member reports that the heating is not following its schedule, gather the details separately; E-110 alone does not establish the cause of that symptom.

Do not ask the member to disclose their Wi-Fi password. Do not infer a cloud outage from E-110 alone: the guide's troubleshooting direction is to check that the router is connected to the internet.

## Router internet checks

Guide the member to check that their router is switched on and connected to the internet. If the household has other ways to check its internet connection, they can use those to establish whether the router currently has internet access.

If the router is not connected to the internet, the member should restore its internet connection using the router or internet service instructions available to them. Once internet access is restored, allow the thermostat to reconnect and check whether E-110 clears.

The thermostat uses a 2.4 GHz Wi-Fi network. A 5 GHz network cannot be used by the thermostat. If the member reports that the Wi-Fi network name or password has changed, use the pairing procedure rather than treating the issue as E-110 alone. Pairing must finish within 3 minutes of the display showing PAIR, and the phone must remain within 5 metres of the thermostat until the app confirms completion.

## What continues to work

While the thermostat cannot reach the Dormouse cloud, it keeps running its schedules. Make this clear to the member: cloud reachability affects communication with the app and cloud services, but the thermostat continues its scheduled operation during the disconnection.

The app may not be able to apply changes to the thermostat while it is disconnected. A change made in the app waits until the thermostat reconnects. Do not advise the member to keep repeating the same change. Repeated changes can make it harder to tell which request they intended to apply.

If the member needs to adjust the target temperature while at the thermostat, they can turn the dial. A manual temperature change lasts until the next schedule period starts.

## Handling delayed app changes

Tell the member that app changes made while the thermostat cannot reach the cloud wait until it reconnects. After internet access is restored, check whether the thermostat has reconnected before asking the member to make another change.

Then have the member check the relevant setting in the app or at the thermostat. If the intended change has not taken effect after reconnection, record the setting, the approximate time it was changed, and what the thermostat currently shows. Do not claim a specific delivery time; the guide does not specify one.

Where the change is time-sensitive, explain the local dial option for changing the target temperature and its duration: a manual change lasts until the next schedule period starts. Do not present this as a way to change schedules, which can only be changed in the app or web dashboard.

## Escalation and resolution notes

If E-110 remains after the member confirms the router is connected to the internet, collect the symptoms and checks completed, then contact Dormouse support through the app at Help > Contact support. Include whether the thermostat is connected to Wi-Fi, whether schedules continue to run, and whether app changes are waiting.

Keep E-110 distinct from boiler fault codes. E-305 indicates that the boiler is not responding; E-312 means the boiler reports a fault. Follow the relevant error-code guidance if either appears.

Close the case when the thermostat can reach the cloud and the member can verify that the expected app change has taken effect, or record the remaining issue for support follow-up. Do not report E-110 as resolved solely because the router has been checked: confirm the thermostat's status or document that reconnection has not yet been observed.
