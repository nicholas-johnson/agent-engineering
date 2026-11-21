---
title: Household Roles and Invitation QA Report
product: app
type: internal
audience: internal
firmware: 4.1
updated: 2026-02-08
---

# Household Roles and Invitation QA Report

## Purpose and scope

This internal QA report covers household roles and invitation behaviour for Dormouse Thermostat firmware 4.1. It checks owner-only device and membership administration, member permissions, the limit of eight household members, and the seven-day invitation expiry.

A household has one owner and can have up to eight members. Members can change the temperature, schedules and away mode. Only the owner can add or remove devices, invite members or remove them.

Invitations are sent from Settings > Household > Invite. The owner enters the invitee's email address, and the invitee receives an email containing a link to join. An invitation works for seven days. After it expires, the owner must send a new invitation.

## Role and permission checks

Validate permissions with one owner account and at least one member account in the same household.

| Action | Owner | Member |
|---|---|---|
| Change target temperature | Allowed | Allowed |
| Change schedules | Allowed | Allowed |
| Turn away mode on or off | Allowed | Allowed |
| Add a thermostat, sensor or valve | Allowed | Not allowed |
| Remove a device | Allowed | Not allowed |
| Invite a household member | Allowed | Not allowed |
| Remove a household member | Allowed | Not allowed |

Confirm that permitted actions take effect for the household. For each owner-only action, verify that a member cannot complete the action. A member must not be able to add or remove a device, invite someone, or remove another member.

The household owner and member permissions are distinct from device roles. Each thermostat controls its own zone and schedule. A home can have up to four Dormouse Thermostats; device administration remains owner-only regardless of how many zones the home has.

## Invitation flow checks

1. Sign in as the owner and open Settings > Household > Invite.
2. Enter an email address and send the invitation.
3. Confirm that the invitee receives an email with a link to join.
4. Open the link and complete the joining flow.
5. Confirm that the new person appears as a household member and can change temperature, schedules and away mode.
6. Confirm that the new member cannot invite or remove members, or add or remove devices.

Also verify that a member account cannot initiate an invitation. The owner is responsible for sending invitations and for removing members.

## Eight-member limit

The household supports up to eight members. Test invitations with a household below the limit, then add members until the household has eight.

At the limit, verify that the household cannot exceed eight members. Check that an invitation sent when the household is already full does not result in a ninth member. Repeat the check after a member is removed: the owner should then be able to invite a replacement, subject to the seven-day invitation flow.

The source behaviour specifies the maximum household size but does not define a particular full-house error message or interface treatment. Record the observed response during QA; do not assume wording or a specific notification.

## Seven-day invitation expiry

Verify an invitation before and after its seven-day validity period. Before expiry, confirm that its link allows the invitee to join. After expiry, confirm that the expired invitation cannot be used to join.

The owner must send a new invitation after the original expires. Confirm that a newly sent invitation has its own seven-day validity period and that the old expired link remains unusable.

The exact expiry boundary and any displayed expiry message are not specified in the product behaviour covered here. Record the observed boundary and message for the tested build without treating either as a guaranteed product requirement.

## Regression checks

Run these checks after changes to household access, invitation handling or account flows:

- Owner can invite a member through Settings > Household > Invite.
- A member cannot send an invitation.
- A valid invitation joins the invitee to the intended household.
- An expired invitation does not grant access; the owner can issue a replacement.
- A household cannot grow beyond eight members.
- Removing a member is owner-only.
- Adding and removing devices is owner-only.
- Members can change temperature, schedules and away mode.
- Existing household members retain their assigned permissions after another member joins or leaves.

Where behaviour differs from these requirements, record the firmware and app or web-dashboard version, account role, household size, steps taken, and observed result.

## Support and reporting notes

For a household-access problem, first establish whether the person is the owner or a member, whether the household already has eight members, and whether the invitation is still within its seven-day validity period. If an invitation has expired, the owner needs to send a new one.

Do not advise a member to perform owner-only administration. If the owner cannot invite or remove members, or cannot add or remove devices, capture the relevant account role, household size and steps to reproduce. Support is contacted in the app under Help > Contact support.

## Release context

Firmware 3.3 increased the household limit from five to eight members and changed invitations to expire after seven days. Firmware 4.1 is the current firmware covered by this report.

When testing a release, compare observed behaviour with the role permissions, limit and expiry requirements in this report. Keep observations about unspecified interface details separate from confirmed requirements.
