---
title: Wi-Fi Connectivity Triage Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-03-18
---

# Wi-Fi Connectivity Triage Playbook

## Purpose and scope

Use this playbook to triage thermostat Wi-Fi issues involving E-101, a Wi-Fi symbol with a cross, or loss of connectivity after a router network name or password changes.

The thermostat requires a 2.4 GHz Wi-Fi network. It cannot join a 5 GHz network. This playbook covers router power and network availability checks, followed by pairing the thermostat again when network credentials have changed.

E-110 is a separate error: it means the thermostat cannot reach the Dormouse cloud. In that case, check that the router is connected to the internet. Do not treat E-110 as evidence that the thermostat cannot find a Wi-Fi network.

## Confirm the symptom

Check the thermostat display and the app for the reported status or error code. The app shows the same error code as the thermostat and can notify the user about it.

| Symptom | Meaning | Initial direction |
|---|---|---|
| E-101 | Wi-Fi network not found | Check router power and whether a 2.4 GHz network is available. |
| Wi-Fi symbol with a cross | Thermostat is not connected to Wi-Fi | Check the network and determine whether its name or password changed. |
| E-110 | Cannot reach the Dormouse cloud | Check the router's internet connection. The thermostat keeps running its schedules; app changes wait until it reconnects. |

Record the code and the user's description before proceeding. Do not assume that a cloud connection problem is a Wi-Fi network discovery problem.

## Check router power

Ask the user to confirm that the router is switched on. If it is off, have them switch it on and allow it to become available before checking the thermostat again.

If the router is already on, continue to the network availability check. E-101 specifically indicates that the Wi-Fi network was not found; it does not, by itself, establish that the router has failed.

Keep the troubleshooting focused on whether the required network is being offered. Avoid treating a router's internet connection as the only relevant check for E-101: the thermostat needs to find a compatible 2.4 GHz network before it can join it.

## Check for a 2.4 GHz network

Confirm that the router offers a 2.4 GHz Wi-Fi network. The thermostat cannot join a 5 GHz network, so availability of a 5 GHz network alone is not sufficient.

If no 2.4 GHz network is available, the thermostat cannot pair with the router. Have the user check the router's network settings or consult the person who manages the router, then retry once a 2.4 GHz network is available.

If the router offers both 2.4 GHz and 5 GHz networks, make sure the pairing process can use the 2.4 GHz network. Do not claim that the thermostat supports 5 GHz or instruct the user to pair it to a 5 GHz network.

## Check whether credentials changed

Ask whether the Wi-Fi network name or password has changed since the thermostat was last connected.

If either has changed, pair the thermostat again. The thermostat must be connected to Wi-Fi and to the user's Dormouse account through pairing. Do not continue treating the old network details as valid after a network name or password change.

If credentials have not changed, return to the router power and 2.4 GHz checks. For a persistent E-101, verify those conditions before attempting another pairing.

## Re-pair after a network change

Use these steps when the router's network name or password has changed, or when the thermostat needs to be paired again after E-101.

1. Hold the thermostat dial down for 5 seconds, until the display shows PAIR.
2. In the Dormouse app, choose Add thermostat and follow the steps.
3. Keep the phone within 5 metres of the thermostat until the app says pairing has finished.

Pairing must finish within 3 minutes of PAIR appearing on the display. If the display shows E-104, pairing timed out. Start again by holding the dial down for 5 seconds, and keep the phone within 5 metres throughout pairing.

## Distinguish E-101, E-104 and E-110

Use the error code to select the next action:

- **E-101 - Wi-Fi network not found:** Check that the router is on and offers a 2.4 GHz network. If the network name or password changed, pair the thermostat again.
- **E-104 - Pairing timed out:** Restart pairing and keep the phone within 5 metres. Complete pairing within 3 minutes of PAIR appearing.
- **E-110 - Cannot reach the Dormouse cloud:** Check that the router is connected to the internet. The thermostat continues running its schedules while disconnected, and changes made in the app wait until it reconnects.

Do not direct an E-110 case to repeat the E-101 checks as the sole response. The codes describe different conditions and have different troubleshooting actions.

## Verify recovery and record outcome

After a successful pairing, confirm that the app reports pairing is complete and that the thermostat no longer displays the Wi-Fi symbol with a cross. If pairing does not finish within the allowed time, use the E-104 procedure and start again.

Record the observed code, whether the router was on, whether a 2.4 GHz network was available, whether the network name or password had changed, and whether pairing completed. If the issue remains, preserve these checks and the exact display code in the support case so the next triage step can distinguish network discovery, pairing timeout and cloud reachability.
