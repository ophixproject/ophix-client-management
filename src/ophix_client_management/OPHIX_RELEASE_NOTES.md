# Ophix Client Management Release Notes

## 2026.10.04.01

- Reworked `README.md`'s opening with a hook-first pitch (fleet-wide token-age and
  client-version visibility, before a stale token becomes a security problem), as part of the
  16-package taskserver-release-wave README overhaul. Also removed the README's leftover
  "successor to `ophix-token-policy`" framing and migration-from-`ophix-token-policy` section —
  that package was never publicly released, so referencing it in a public README was
  meaningless to anyone reading the repo.

## 2026.09.26.02

- i18n regression check: the Status dashboard page title, the rotation-flagged/no-overdue-clients admin messages, and `check_client_updates`'s "no packages registered" message were unwrapped (the rotation count also used manual pluralization instead of `ngettext`). All wrapped now, matching the file's own existing convention.

## 2026.09.26.01

- Verified real compatibility under Python 3.14 (not just added the classifier) as part of the taskserver-release-wave compatibility sweep, and added `Programming Language :: Python :: 3.14` to the package classifiers.

## 2026.08.31.01

- Client change view "Last token rotation" display reverted to two lines (undoing
  the `2026.08.30.02` single-line merge) — date on top, coloured status label
  underneath, matching the original layout. The status label is now
  `font-weight: 600` across every state (previously only Locked/Unlocked/
  Requested were bold), matching the same label's weight in the Token Status
  column and Status page table.

## 2026.08.30.02

- Fixed token-age text ("Warning (1 days)") always using the plural form
  regardless of count, and never being translatable — three occurrences (Core >
  Clients "Token Status" column, Client change view's token section, and the
  Status page table) all built the string with plain Python `.format()`/a bare
  `"days"` literal. `columns.py`/`admin_fields.py` now use `ngettext` for
  correct singular/plural selection; the Status page template now uses
  `{% blocktrans count %}` instead of the `pluralize` filter, which handled
  plural but not translation.

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
