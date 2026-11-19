---
title: Create a Smart-Home Heating Routine
product: thermostat
type: integration
audience: customer
firmware: 4.1
updated: 2025-07-28
---

# Create a Smart-Home Heating Routine

## Keep temperature schedules on Dormouse

A smart-home routine can respond to Dormouse heating state without taking over temperature control. Let the thermostat manage its schedule and target temperatures. Use your home automation system to decide what other devices or actions should respond when heating is active or inactive.

This separation keeps heating schedules in one place. A routine can, for example, switch a compatible smart plug or trigger another home action when heating starts or stops. It should not repeatedly change the target temperature to imitate a schedule that is already set on Dormouse.

## Check your Dormouse setup

The Dormouse Thermostat needs a 2.4 GHz Wi-Fi network for its connection to the Dormouse app and web dashboard. It is wired to the boiler by a qualified installer. Make sure it is paired and working before building a routine around it.

A home can have up to four Dormouse Thermostats. Each thermostat controls its own zone and has its own schedule. If your home has more than one thermostat, identify which zone the routine should follow. Do not assume that heating state for one zone represents every zone in the home.

Dormouse Radiator Valves and Room Sensors communicate with their zone's thermostat over a low-power radio link. They do not use Wi-Fi themselves. The thermostat is the device to consider when connecting Dormouse heating state to another system.

## Choose a heating-state trigger

In your home automation system, look for an available Dormouse heating-state signal or event. The exact names and setup steps depend on that system, so follow its instructions for connecting devices and creating routines.

Use the heating state as the trigger, rather than the room temperature or target temperature, when the routine should respond to the thermostat actually asking for heat. The thermostat display shows a flame when it is asking the boiler for heat.

A heating-state trigger is not the same as a schedule period being active. A scheduled target can be in effect without the thermostat asking for heat at that moment. Likewise, the thermostat can ask for heat for reasons other than a routine you create, including frost protection.

## Set the routine's actions

Choose actions that make sense when heating starts and when it stops. For example, a routine might switch a compatible device on while the relevant zone is asking for heat, then switch it off when that heating state ends.

Keep those actions separate from the thermostat's control of the boiler. A smart plug or other automation action should not interrupt power to the thermostat or its heating system. The thermostat is mains-powered through its wall plate, and it cannot switch the heating on while mains power is off.

If you use more than one zone, create a clear mapping between each thermostat's heating state and the actions for that zone. Avoid using one zone's state to control devices that should follow another zone.

## Leave temperature control to Dormouse

Set the temperatures and times you want in the Dormouse schedule. Each day can have up to six periods, and each period lasts until the next one starts. Edit schedules in the Dormouse app or web dashboard. The thermostat's Schedule menu shows today's periods but does not let you change them.

Manual temperature changes last until the next schedule period starts. Away mode keeps the home at its configured away temperature until it is turned off. Frost protection is always on and cannot be turned off; it heats if the room falls below 5 degrees, even when heating is off or away mode is on.

Avoid routines that continually change the target temperature, switch heating modes unexpectedly, or attempt to replace these built-in behaviours. If you want to alter a scheduled temperature, change the Dormouse schedule instead.

## Account for ordinary heating behaviour

A heating-state routine should account for the fact that the thermostat may request heat at different times and for different reasons. The target temperature, current room temperature, schedule, away mode and frost protection all affect heating operation.

Do not treat the heating state as a guarantee that every radiator or room is warm. Each thermostat controls its own zone, and a Dormouse Radiator Valve can regulate its own radiator temperature within that zone. A routine can respond to the thermostat's heating state, but it does not replace the thermostat, boiler or zone controls.

If the thermostat is disconnected from the Dormouse cloud, it keeps running its schedules. Changes made in the app wait until it reconnects. Your home automation system may handle a loss of connection differently; check its status and behaviour rather than assuming the routine has current information.

## Test and maintain the routine

Test the routine with a simple action that is easy to observe. Confirm that the chosen thermostat and zone trigger the intended action when heating state changes, and that the action stops or reverses as intended. If the automation system offers a history or activity view, use it to check which trigger and action ran.

Keep the routine independent of target-temperature changes. If you adjust a schedule, away temperature or boost temperature in Dormouse, the routine should continue to respond to heating state rather than trying to recreate those settings.

Dormouse heating history is kept for two years. Use the Dormouse app or web dashboard to review schedules and settings, and use your home automation system's own controls to inspect its routines.

## Troubleshoot carefully

If the routine does not run, first check that the correct Dormouse thermostat is paired, online and associated with the intended zone. Check the automation system's connection and permissions using its own instructions.

If Dormouse shows an error, the app displays the same code as the thermostat and can notify you about it. For example, E-110 means the thermostat cannot reach the Dormouse cloud; it continues running schedules, while app changes wait until reconnection. E-217 means the temperature sensor is disconnected and the thermostat turns heating off to be safe. Follow the instructions for the displayed error rather than trying to compensate with an automation routine.

For help with Dormouse, use Help > Contact support in the app.
