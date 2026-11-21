---
title: Power Interruption and Schedule Continuity QA Report
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-03-02
---

# Power Interruption and Schedule Continuity QA Report

## Purpose and scope

This report documents expected backup-battery behaviour when mains power to a Dormouse Thermostat is interrupted. It covers clock and schedule retention, heating operation during an outage, battery status and the checks needed to assess schedule continuity after power returns.

The report applies to the Dormouse Thermostat with firmware 4.1. It describes product behaviour and QA checks; it does not specify an outage duration beyond the documented backup-battery limit.

## Expected behaviour

Two AA backup batteries, fitted behind the front cover, keep the thermostat's clock and schedules during a power cut for up to 48 hours. The batteries do not provide power for heating control: while mains power is off, the thermostat cannot switch the heating on.

| Condition | Expected behaviour |
|---|---|
| Mains power available | The thermostat operates using mains power. |
| Mains power interrupted | The thermostat runs on its backup batteries. It keeps the clock and schedules for up to 48 hours, but cannot switch the heating on. |
| Backup batteries low | The thermostat shows E-401. Replace the two AA batteries within a month. |
| Mains power interrupted, E-402 shown | The thermostat is running on backup batteries and cannot switch the heating on. |

Do not treat retained schedules as evidence that the heating can operate during an outage. Schedule and clock retention are distinct from the ability to energise the heating.

## QA test objectives

Verify that:

1. The thermostat retains its clock and schedules during a mains outage within the documented backup period.
2. The thermostat does not switch on the heating while mains power is off.
3. The thermostat indicates mains interruption with E-402 when applicable.
4. A low backup-battery condition is indicated with E-401.
5. After mains power returns, the retained schedule remains available for normal operation.

The guide specifies retention for up to 48 hours. This report does not define behaviour beyond that limit or prescribe a particular recovery sequence after an outage exceeding it.

## Test setup and preparation

Use a Dormouse Thermostat with firmware 4.1, wired to a compatible gas boiler by a qualified installer. Record the firmware version from Menu > About before testing.

Before the test:

1. Confirm the thermostat is operating with mains power.
2. Set a recognisable schedule in the app or web dashboard. Each day can have up to six periods; each period has a start time and target temperature.
3. Record the displayed room and target temperatures and the schedule periods relevant to the test.
4. Confirm the backup batteries are present and note any displayed error code.
5. Arrange a safe, controlled mains interruption through the appropriate installation setup. Do not handle wiring unless qualified to do so.

Schedule changes are made in the app or web dashboard. On the thermostat, Menu > Schedule shows today's periods but does not allow them to be changed.

## Test procedure

1. With mains power available, confirm that the thermostat is operating and that the prepared schedule is present.
2. Interrupt mains power using the controlled test setup.
3. Observe the thermostat and record any error code. E-402 indicates that the thermostat is running on backup batteries because mains power is interrupted.
4. Confirm that the thermostat cannot switch the heating on while mains power remains off. Do not infer heating operation from a retained target temperature or schedule.
5. Maintain the interruption only for a duration within the documented backup period of up to 48 hours. Record the elapsed time.
6. Restore mains power using the controlled test setup.
7. Check that the clock and schedule are retained, and record the thermostat's displayed status and any error code.

This procedure verifies the documented behaviours. It does not establish guaranteed retention after 48 hours or define recovery timing beyond what is stated in the user guide.

## Pass and fail criteria

**Pass** when, during an outage within the documented period:

- The thermostat runs on its backup batteries.
- The clock and schedules are retained.
- The thermostat does not switch the heating on while mains power is off.
- E-402 is shown when the thermostat indicates mains interruption.

After mains power returns, the schedule should remain available as recorded before the test.

**Fail** if the thermostat switches the heating on without mains power, or if the clock or schedules are not retained during an outage within the documented period. Record the firmware version, elapsed outage time, observed display state and schedule before and after the test. Do not report conclusions about outages longer than 48 hours as failures against the documented retention period.

## Error-code handling

| Code | QA interpretation | Action |
|---|---|---|
| E-402 | Mains power is interrupted; the thermostat is running on backup batteries. It keeps the clock and schedules for up to 48 hours but cannot switch the heating on. | Check the mains supply and restore it when appropriate. |
| E-401 | Backup batteries are low. | Replace the two AA batteries behind the front cover within a month. |

The batteries are accessed by gently pulling the bottom of the front cover towards you. The guide recommends replacing them once a year, or when E-401 appears. Do not confuse E-401 with E-402: one reports low backup batteries, the other reports interrupted mains power.

## Support and reporting notes

When documenting an incident or test, distinguish clearly between:

- **Schedule retention:** whether the clock and programmed periods remain available.
- **Heating operation:** whether the thermostat can switch on heating. It cannot do so while mains power is off.
- **Power status:** whether E-402 is displayed.
- **Battery condition:** whether E-401 is displayed.

For support, contact Dormouse in the app under Help > Contact support. Include the firmware version, error code, outage duration, battery status and schedule observations. Avoid promising schedule retention beyond the documented period of up to 48 hours.
