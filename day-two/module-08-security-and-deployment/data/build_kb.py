# Copies a small part of Module 6's knowledge base into data/kb/: the documents about
# warranties, replacements, households and privacy, for customers and for staff.
# Run from the module folder: uv run python data/build_kb.py

import shutil
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE.parents[1] / "module-06-rag-and-proprietary-knowledge" / "data" / "docs"
KB = HERE / "kb"

FOR_CUSTOMERS = [
    "change-the-target-temperature.md",
    "check-your-thermostat-hardware-revision.md",
    "contact-dormouse-support-in-the-app.md",
    "factory-reset-the-thermostat.md",
    "heating-history-data-retention-policy.md",
    "identify-your-thermostat-hardware-revision.md",
    "invitation-to-join-a-household-has-expired.md",
    "invite-someone-to-your-home.md",
    "manage-household-access-for-connected-controls.md",
    "manage-household-member-permissions.md",
    "manage-location-sharing-for-household-members.md",
    "phone-location-privacy-policy.md",
    "reset-your-dormouse-account-password.md",
    "return-a-dormouse-product-within-the-returns-period.md",
    "returns-policy.md",
    "set-a-heating-schedule.md",
    "set-up-geofencing.md",
    "thermostat-electrical-safety-policy.md",
    "thermostat-replacement-on-an-existing-wall-plate.md",
    "thermostat-warranty-policy.md",
    "turn-away-mode-on-or-off.md",
    "turn-on-two-step-verification.md",
    "understand-heating-history-retention.md",
    "understand-household-invitation-expiry.md",
    "understand-how-location-privacy-works-with-geofencing.md",
    "understand-the-dormouse-product-warranty.md",
    "understand-the-thermostat-display-and-dial.md",
    "understand-warm-wake.md",
    "understand-what-a-factory-reset-removes.md",
    "understand-who-can-manage-a-dormouse-home.md",
]

FOR_STAFF = [
    "account-sign-in-and-recovery-qa-report.md",
    "away-mode-and-geofencing-qa-report.md",
    "boiler-fault-triage-playbook.md",
    "heating-history-retention-and-location-privacy-notes.md",
    "household-notification-preferences-support-notes.md",
    "household-roles-and-invitation-qa-report.md",
    "internal-relay-click-revision-c.md",
    "network-disconnection-known-issues.md",
    "temperature-sensor-fault-escalation-playbook.md",
    "thermostat-firmware-release-history.md",
    "thermostat-hardware-revision-identification.md",
    "warm-wake-known-issue-register.md",
]

shutil.rmtree(KB, ignore_errors=True)
KB.mkdir()
for name in FOR_CUSTOMERS + FOR_STAFF:
    shutil.copy(SOURCE / name, KB / name)
print(f"Copied {len(FOR_CUSTOMERS)} documents for customers and {len(FOR_STAFF)} for staff to data/kb/")
