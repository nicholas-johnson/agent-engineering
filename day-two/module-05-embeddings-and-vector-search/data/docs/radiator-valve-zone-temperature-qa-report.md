---
title: Radiator Valve Zone Temperature QA Report
product: radiator valve
type: internal
audience: internal
firmware: 4.1
updated: 2026-03-15
---

# Radiator Valve Zone Temperature QA Report

## Purpose and scope

This report defines checks for adding Dormouse Radiator Valves to a zone and confirming that each joined radiator heats to its own temperature. It is an internal QA document for the Dormouse Thermostat with firmware 4.1.

A home can have up to four thermostats, each controlling its own zone and schedule. Up to ten Dormouse Radiator Valves can join one zone. Each valve controls the temperature of its own radiator; the zone thermostat manages that zone.

Valves communicate with their zone's thermostat over a low-power 868 MHz radio link. Only the thermostat uses Wi-Fi. These checks cover setup, zone membership, temperature control and relevant failure handling. They do not define a valve temperature range or a user interface not specified in the product documentation.

## Test setup and preconditions

Use a functioning Dormouse Thermostat and the Dormouse app or web dashboard. Confirm that the thermostat is paired and connected, and identify the zone under test. Use a separate thermostat for each additional zone being tested.

Prepare up to ten valves for the zone. The Dormouse Radiator Valve fits M30 x 1.5 valve bodies; adapters in the box support other common valves. Each valve runs on two AA batteries, which last about two years. Check that each valve is correctly fitted to its radiator and has working batteries before testing.

Record the thermostat firmware, zone identity, valve count, radiator identity and assigned test temperature for each valve. The current firmware is 4.1. Do not infer a temperature range, accuracy or response time for radiator valves from the thermostat specifications.

## Adding a valve to a zone

Add each valve through the documented device flow:

1. In the app or web dashboard, go to Settings > Home > Add a device.
2. Follow the presented steps to add the valve.
3. Confirm that the valve is associated with the intended zone.
4. Repeat for further valves, keeping the total at or below ten in that zone.

Verify that the valve is not mistakenly assigned to another zone. Where the home has multiple thermostats, check the zone identity before evaluating heating behaviour. Record whether each valve appears as an added device in the product interface; do not treat undocumented display labels or status indicators as pass criteria.

If setup does not complete, capture the observed interface and device configuration. Do not attribute a failure to Wi-Fi without evidence: valves use the 868 MHz link to the zone thermostat, while Wi-Fi is used by the thermostat.

## Independent radiator temperature check

The main functional check is that each joined radiator can heat to its own temperature, rather than being forced to follow another valve's individual setting.

With two or more valves in the same zone:

1. Assign a distinct test temperature to each valve using the available product controls.
2. Confirm that each valve remains associated with its intended radiator and zone.
3. Allow the heating system to operate under the test conditions.
4. Observe each radiator separately and record whether it heats in accordance with its own assigned temperature.
5. Change one valve's temperature and check that the change does not replace the individual setting of another valve.

Use settings that are distinguishable from one another, without assuming an undocumented minimum difference or temperature step for valves. Assess the result against the valve's own assigned temperature, not solely against the room temperature reported by the thermostat. The thermostat measures and controls its zone; a Dormouse Room Sensor may also join a zone to measure temperature in another room, but that does not change the requirement that each joined radiator heats to its own temperature.

## Coverage and boundary checks

Run the independent-temperature check with at least two valves, then repeat with additional valves where capacity permits. Include a check with ten valves in one zone to cover the documented zone limit. Do not interpret a failed attempt to add an eleventh valve as evidence of a defect without first confirming the zone already contains ten valves.

Where multiple zones are available, add valves to the intended zone and verify that the test records distinguish them from valves in other zones. A home supports up to four thermostats, each with its own zone and schedule. Do not count valves in separate zones against the ten-valve limit for the zone under test.

Check the basic installation context when a radiator does not heat as expected: correct radiator, correct valve, correct zone, battery condition and boiler operation. The thermostat's E-305 guidance includes checking that the boiler is switched on and its pressure is between 1 and 1.5 bar, then checking the boiler's own display for a fault. E-312 indicates a fault reported by the boiler.

## Fault handling and evidence

The product documentation does not specify a radiator-valve error-code table. Do not assign thermostat error meanings to a valve or invent recovery steps. Record the exact device, zone, observed behaviour and any code shown by the thermostat or app.

If the thermostat shows E-110, it cannot reach the Dormouse cloud. The thermostat continues running schedules, and app changes wait until it reconnects. This is distinct from the valve-to-thermostat radio link; capture the condition without concluding that E-110 proves a valve communication fault.

For any unsuccessful check, preserve:

- Thermostat firmware and zone identity.
- Number of valves in the zone and each valve's radiator.
- The individual temperature assigned to each valve.
- Setup steps completed and the observed result for each radiator.
- Relevant thermostat or app error codes and the state of mains power, boiler and batteries.

Contact support through the app at Help > Contact support when escalation is needed. Include the evidence above and avoid claiming a cause that the checks have not established.

## Pass and fail criteria

**Pass** when each valve is added to the intended zone, the zone contains no more than ten valves, and each tested radiator heats in accordance with its own assigned temperature. Changing one valve's setting must not overwrite another valve's individual setting.

**Fail** when a valve cannot be associated with the intended zone through the documented add-device flow, the zone exceeds its supported valve count, or a radiator does not respond in accordance with its own assigned temperature after setup and relevant boiler and power conditions have been checked.

Mark a result **inconclusive** when the test cannot isolate valve behaviour from a boiler fault, power interruption, incorrect installation or other unresolved condition. Record the evidence and arrange follow-up rather than treating an inconclusive result as a pass.
