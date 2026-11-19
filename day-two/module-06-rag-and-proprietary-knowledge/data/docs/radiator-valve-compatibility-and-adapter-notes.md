---
title: Radiator Valve Compatibility and Adapter Notes
product: radiator valve
type: internal
audience: internal
firmware: 4.1
updated: 2025-07-14
---

# Radiator Valve Compatibility and Adapter Notes

## Purpose and scope

This internal note covers compatibility and setup considerations for the Dormouse Radiator Valve. It is intended to help engineering, support and QA teams describe the product accurately and handle compatibility enquiries consistently.

The Radiator Valve joins a Dormouse Thermostat zone and controls the temperature at its own radiator. A zone can have up to ten Radiator Valves. Valves communicate with the thermostat for their zone over a low-power 868 MHz radio link. They do not connect directly to Wi-Fi; only the thermostat uses Wi-Fi.

## Valve-body compatibility

The Radiator Valve fits M30 x 1.5 valve bodies. The product box includes adapters for other common valve bodies.

Do not describe the supplied adapters as supporting every non-M30 x 1.5 valve body. The available compatibility information identifies them only as adapters for other common valves; it does not specify a complete list of compatible valve-body types or adapter-to-body mappings.

When responding to a compatibility enquiry, establish the valve-body type before advising that the product will fit. If the body is not M30 x 1.5 and its compatibility with a supplied adapter cannot be confirmed from approved product information, do not promise a fit. Escalate the enquiry through the support process rather than inferring compatibility from appearance.

## Supplied adapters

Adapters are included in the box for other common valve bodies. Their purpose is to allow the Radiator Valve to fit valve bodies other than the standard M30 x 1.5 type.

The product information does not provide adapter names, measurements, installation instructions or an exhaustive list of supported bodies. Do not invent adapter identifiers or claim a specific body type is supported unless that information is confirmed in approved compatibility material.

For support and documentation, distinguish between these statements:

- **Confirmed:** the Radiator Valve fits M30 x 1.5 valve bodies.
- **Confirmed:** adapters are supplied for other common valve bodies.
- **Not specified here:** which individual valve-body types each adapter fits.

## Battery requirements

The Radiator Valve runs on two AA batteries. The batteries last about two years.

Keep this requirement distinct from the thermostat's backup batteries. The thermostat's two AA backup batteries are behind its front cover and keep the clock and schedules during a mains power cut; they do not power the Radiator Valve. Do not apply thermostat battery behaviour, replacement timing or error-code guidance to a Radiator Valve unless separately confirmed for that product.

## Zone and radio-link context

Each thermostat controls its own zone and schedule. A Dormouse Radiator Valve can join a zone so that the radiator it controls heats to its own temperature. Up to ten Radiator Valves can join a single zone.

Valves communicate with their zone's thermostat over a low-power 868 MHz radio link. Wi-Fi setup applies to the thermostat, not to an individual valve. When explaining the system, avoid telling users to connect a Radiator Valve to their Wi-Fi network.

## Support handling

Use the following sequence when assessing a fit enquiry:

1. Confirm that the product in question is the Dormouse Radiator Valve.
2. Ask for the valve-body type or other identifying information available to the customer.
3. If the body is confirmed as M30 x 1.5, state that this is a supported fit.
4. If it is another common valve body, explain that adapters are included, but do not guarantee compatibility with a particular body unless confirmed by approved product information.
5. If compatibility remains uncertain, contact Dormouse support in the app under Help > Contact support.

Keep guidance factual. Do not advise users to force, modify or improvise an adapter fit. No such installation method is specified in the product information.

## QA checks and documentation boundaries

QA and documentation reviews should check that Radiator Valve compatibility statements retain the distinction between the confirmed M30 x 1.5 fit and the more general statement that adapters are supplied for other common valve bodies.

Check that product descriptions and support responses:

- state that the valve uses two AA batteries and that they last about two years;
- describe the 868 MHz link as communication between a valve and its zone's thermostat;
- make clear that only the thermostat uses Wi-Fi;
- do not present the thermostat's backup-battery instructions as Radiator Valve instructions; and
- do not claim support for a specific non-M30 x 1.5 body without confirmation.

## Internal rollout and verification notes

Before publishing revised compatibility wording or changing support guidance, verify the claims against approved product information and relevant test coverage. Confirm that edits do not turn "other common valve bodies" into an unsupported exhaustive compatibility list, or imply that all supplied adapters fit all non-M30 x 1.5 bodies.

Firmware rollout follows the internal staged process: release to 1% of thermostats, then 10%, then all thermostats over a week. Every release is tested against the manual test-script library before rollout. These are rollout and verification controls; they do not establish additional Radiator Valve body compatibility or installation guidance.
