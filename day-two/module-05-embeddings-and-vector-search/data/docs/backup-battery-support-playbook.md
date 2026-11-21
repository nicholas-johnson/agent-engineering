---
title: Backup Battery Support Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-08-08
---

# Backup Battery Support Playbook

## Purpose and scope

This playbook covers the Dormouse Thermostat's backup batteries and the two related error codes:

- **E-401:** Backup batteries low.
- **E-402:** Mains power interrupted.

Use it to explain the warning, guide a customer through battery replacement and clarify what the thermostat can and cannot do while mains power is off. It applies to the Dormouse Thermostat with firmware 4.1.

The thermostat uses two AA backup batteries to keep its clock and schedules during a power cut, for up to 48 hours. These batteries do not power the heating controls: while mains power is off, the thermostat cannot switch the heating on.

## How the backup batteries work

The batteries are a backup for the thermostat's clock and schedules, not an alternative power supply for heating. If mains power is interrupted, the thermostat can preserve the clock and schedules for up to 48 hours, but it cannot call for heat.

The batteries are located behind the thermostat's front cover. The cover's bottom edge pulls gently towards you to give access. The thermostat is wired to the boiler by a qualified installer; battery replacement does not change that wiring.

Explain the distinction clearly when handling a report of a cold home during a power cut: the thermostat's backup batteries can maintain the clock and schedules, but they cannot operate the heating without mains power.

## E-401: Backup batteries low

E-401 means the backup batteries are low. The warning appears a month before the batteries run out. The customer should replace both AA batteries within that month.

The recommended routine is to replace the batteries once a year, or sooner if E-401 appears. Do not describe E-401 as a mains-power fault: it is specifically a low-battery warning.

The thermostat may also notify a customer that the backup batteries are low if that member has enabled the relevant notification in Settings > Notifications. The display error code and the app show the same code.

## E-402: Mains power interrupted

E-402 means mains power has been interrupted and the thermostat is running on its backup batteries. It can keep the clock and schedules for up to 48 hours, but it cannot switch the heating on while mains power is off.

Tell the customer that E-402 does not mean the batteries have failed. It indicates loss of mains power. If the heating is unavailable during the interruption, this is an expected limitation of backup operation.

If mains power remains off beyond the backup period, do not promise that the thermostat will continue keeping the clock and schedules. The guide specifies a period of up to 48 hours.

## Battery replacement procedure

Ask the customer to replace the two AA batteries behind the front cover. The guide specifies the battery type and access point, but does not specify battery polarity, a reset procedure or a confirmation step. Do not invent instructions for these.

1. Locate the bottom edge of the thermostat's front cover.
2. Pull the bottom of the cover gently towards you.
3. Replace the two AA backup batteries.
4. Refit the front cover.

If the customer cannot access the batteries or needs help beyond these steps, direct them to Help > Contact support in the app. Do not ask them to handle the boiler wiring; the thermostat must be wired to the boiler by a qualified installer.

## Support handling and customer messaging

Use plain, direct language:

- For **E-401**, explain that the two AA backup batteries are low and should be replaced within a month.
- For **E-402**, explain that mains power is interrupted. The thermostat can preserve its clock and schedules for up to 48 hours, but cannot switch on the heating without mains power.
- For either code, distinguish the battery warning from the mains interruption. Do not imply that replacing batteries will restore mains power or enable heating during a power cut.

The app shows the same error code as the thermostat and can notify the customer about it. Notification preferences are set individually under Settings > Notifications. If the customer needs further assistance, support can be contacted in the app under Help > Contact support.

## QA and verification notes

Check that customer-facing guidance and support responses preserve these distinctions:

| Check | Correct behaviour or guidance |
|---|---|
| E-401 meaning | Backup batteries low |
| E-401 action | Replace the two AA batteries within a month |
| Routine replacement | Replace batteries once a year, or when E-401 appears |
| E-402 meaning | Mains power interrupted; thermostat is on backup batteries |
| Backup duration | Clock and schedules are kept for up to 48 hours |
| Heating during mains interruption | The thermostat cannot switch the heating on |
| Battery access | Pull the bottom of the front cover gently towards you |

Do not claim that the backup batteries keep the heating running, or that E-402 is resolved by replacing batteries. Do not give unsupported battery-handling steps or a battery life estimate beyond the guide's stated backup duration.
