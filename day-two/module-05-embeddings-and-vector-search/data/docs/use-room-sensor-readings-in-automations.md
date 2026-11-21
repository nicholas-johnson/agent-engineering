---
title: Use Room Sensor Readings in Automations
product: room sensor
type: integration
audience: customer
firmware: 4.1
updated: 2025-11-21
---

# Use Room Sensor Readings in Automations

## Overview

A Dormouse Room Sensor measures temperature and humidity in a room. You can use those readings as inputs to compatible home automation rules, such as rules that respond when a temperature or humidity reading reaches a value you choose.

The Room Sensor joins a Dormouse Thermostat's zone. Its readings are associated with that zone, so check that the sensor is in the zone you intend to use. A zone can have up to three Dormouse Room Sensors.

The Room Sensor does not connect to Wi-Fi. It communicates with the thermostat for its zone over a low-power 868 MHz radio link. The thermostat is the device that connects to Wi-Fi.

## What you need

Before setting up an automation, make sure you have:

- A Dormouse Thermostat paired with your Dormouse account.
- A Dormouse Room Sensor added to the zone whose readings you want to use.
- A compatible home automation system that can use Dormouse temperature and humidity readings as rule inputs.

To add a Room Sensor, go to Settings > Home > Add a device. Follow the instructions in the app or web dashboard to join it to a zone.

The sensor measures both temperature and humidity. Your home automation system determines which readings it can use and what rule options it provides. Refer to that system's instructions for its available triggers, conditions and actions.

## Choose a suitable rule

A rule uses a sensor reading as an input and performs an action when its conditions are met. For example, you might use a temperature reading to trigger an action when the reading is above or below a value. A compatible system may also let you use humidity readings.

Choose values and actions that suit the room and the equipment controlled by your automation. A reading from one sensor describes the conditions where that sensor is placed; it may not represent other rooms in the same zone or home.

Dormouse does not define the rules or actions in another home automation system. Check that system's instructions for how to select a Dormouse Room Sensor and configure its readings as inputs.

## Configure an automation

The exact steps depend on the compatible system. In general:

1. Open the rule or automation editor in that system.
2. Choose a Dormouse Room Sensor in the zone you want to monitor.
3. Select temperature or humidity as the reading to use.
4. Set the condition and value required by your rule.
5. Choose the action the rule should perform.
6. Save the rule and check the system reports that it is active.

If the system lists more than one sensor, confirm you have selected the right one. Give sensors clear identifiers in the system if it supports them, so you can tell them apart.

## Keep sensors in the right zone

Each Dormouse Room Sensor belongs to a zone controlled by a Dormouse Thermostat. A home can have up to four Dormouse Thermostats, each with its own zone and schedule. Make sure you add the sensor to the zone whose readings your automation needs.

If you move a sensor or change the setup of your home, check that it remains in the intended zone and that the automation still uses the correct sensor. Adding a sensor to one zone does not make its readings a measurement of another zone.

## Check readings and automations

After setup, check the readings shown in the Dormouse app or web dashboard and compare them with what your automation system reports. Allow for differences in how systems display or update readings.

If an automation does not run as expected:

- Confirm the rule is enabled in the home automation system.
- Check that it uses the intended Dormouse Room Sensor and reading.
- Check the condition, value and action in the rule.
- Confirm the sensor is still joined to the intended zone.
- Check whether the system indicates that its Dormouse connection or sensor data is unavailable.

The automation system controls its own rules and actions. A change to a rule there does not change the thermostat's schedule or settings.

## Sensor power and care

The Dormouse Room Sensor runs on one CR2032 coin cell, which typically lasts about a year. Replace the battery when required, following the instructions supplied with the sensor. After replacing it, check that the sensor is reporting readings and that any rules using those readings are still active.

Place the sensor where it can measure the room you want to monitor. Avoid treating one sensor's reading as a measurement of the whole home. For cleaning, use a soft, dry cloth. Do not use sprays or cleaning products, and do not paint over the sensor.

## Privacy and support

Phone locations used for Dormouse geofencing are not stored. Dormouse stores only whether each household member is home or away. Room Sensor readings are separate from this location information.

For help with adding a sensor or checking its readings, contact Dormouse support in the app under Help > Contact support. For help configuring a rule, check the instructions for the compatible home automation system.
