# Ophix Client Management Release Notes

## Unreleased

- Client change view: "Last token rotation" is now a single line — the date renders
  with the same locale-aware `DATETIME_FORMAT` Django uses when ophix-client-management
  isn't installed, followed inline by the coloured status label and age (e.g.
  "31 May 2026, 2:47 p.m.  OK (5 days)"). Previously this was two lines: a coloured
  status line on top and a plain ISO-style date beneath it.

## 2026.06.24.01

- Client change view now shows "Last token rotation" as a styled status indicator
  (OK / Warning / Rotation Required / Requested by Operator / Locked / Never Rotated)
  with age in days and the raw date beneath it, matching the visual style of the Status
  dashboard. Requires `ophix-server-base>=2026.06.24.01`.

## 2026.06.23.01

- Initial release — successor to `ophix-token-policy`.
- Identical functionality: token rotation policy management, client version tracking, Status dashboard.
- Left nav section renamed from "Token Policy" to "Client Management".
- Dashboard page renamed from "Token Policy" to "Status".
- Admin URL changed from `/token-policy/` to `/client-management/`.
- Django app label changed from `ophix_token_policy` to `ophix_client_management` (fresh DB tables on install).
- Env var to control sidebar visibility renamed from `SHOW_TOKEN_POLICY_MODEL` to `SHOW_CLIENT_MANAGEMENT_MODEL`.
- `ClientVersion` rows rebuild automatically as fleet clients reconnect.
- Run `check_client_updates` to repopulate the `ClientPackageVersion` table after switching.
