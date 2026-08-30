# Ophix Client Management Release Notes

## 2026.08.30.01

- Core > Clients "Token Status" column: all states now render with `font-weight: 600`
  (previously only Locked/Requested were bold, so most rows looked lighter-weight
  than the rest of the changelist).
- Status page (`/client-management/`) table headers now match Django's own changelist
  header styling: `font-size: 0.6875rem`, `color: var(--body-quiet-color)` (was
  `0.85em` in the theme's module-background colour, with a separate dark-mode
  override that's no longer needed since `--body-quiet-color` is already
  theme/dark-mode aware).
- Status page "Version" column: removed the `0.85em` font-size override so it
  matches the rest of the table's text size.
- Status page "Status" column: combined the status label and age into a single line
  of coloured text (e.g. "Warning (14 days)"), matching the pattern used on the
  Client change view's token section. Previously this was two stacked lines (a
  coloured status label, then a separate muted age line below it); removed the now
  -unused `.age-label` rule.
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
