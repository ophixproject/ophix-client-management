# ophix-client-management

**Know which fleet clients need attention, before a stale token becomes a security problem.**

Client tokens don't rotate themselves, and a forgotten one sitting unrotated for months (or years) is exactly the kind of thing that only surfaces during an audit — or an incident. `ophix-client-management` gives you a fleet-wide status dashboard showing every client's token age and reported software version at a glance, lets you request rotation or lock out a client directly from the admin, and enforces a hard rotation deadline automatically once you've configured one.

---

## Installation

```bash
pip install ophix-client-management
ophix-manage migrate
```

The plugin registers itself automatically via the `ophix.plugins` entry point — no changes
to `INSTALLED_APPS` or `MIDDLEWARE` are needed.

---

## What this plugin provides

- Status dashboard at `/client-management/` — linked from the admin left-hand nav under **Client Management**
- Per-client status bars with six states: OK / Warning / Rotation Required / Locked / Never Rotated / Operator Requested
- Per-client actions: **Request Rotation**, **Clear Request**, **Unlock Client**
- Bulk **Request Rotation — All Overdue** action
- `X-Token-Rotation-Warning: true` response header injected for clients in the warn state
- `X-Token-Rotation-Required: true` response header injected for clients past the require threshold or operator-flagged
- Hard lockout enforcement in `ClientTokenAuthentication` — clients past `TOKEN_LOCKOUT_DAYS` are denied API access until an operator unlocks them from the dashboard
- Client version tracking — captures the `X-*-Client-Version` request header on every successful API call and displays the last-seen version per client in the dashboard

---

## Dashboard states

| State | Meaning |
|---|---|
| **OK** | Token age below warn threshold — no action needed |
| **Warning** | Token age between warn and require thresholds — `X-Token-Rotation-Warning` sent |
| **Rotation Required** | Token age past require threshold — `X-Token-Rotation-Required` sent |
| **Locked** | Token age past lockout threshold — API access blocked until operator unlocks |
| **Never Rotated** | No rotation recorded — lockout does not apply |
| **Operator Requested** | Flagged manually via the dashboard — `X-Token-Rotation-Required` sent |

---

## Configuration (`.env`)

| Variable | Default | Purpose |
| --- | --- | --- |
| `TOKEN_WARN_DAYS` | `30` | Age (days) at which the warning signal is sent |
| `TOKEN_REQUIRE_DAYS` | `90` | Age (days) at which the required signal is sent |
| `TOKEN_LOCKOUT_DAYS` | `180` | Age (days) at which API access is blocked. Set to `0` to disable lockout. A value below `TOKEN_REQUIRE_DAYS` is invalid and will be ignored with a log warning. |

Recommended values are shown above. `TOKEN_LOCKOUT_DAYS` must be greater than or equal to
`TOKEN_REQUIRE_DAYS` to take effect.

---

## Client signalling and automatic rotation

Tier 1 clients built on `ophix-client-core` check the rotation signal headers automatically
on every API response. Two env vars in each client's domain env file control the behaviour:

| Variable | Default | Purpose |
| --- | --- | --- |
| `ROTATE_ON_WARNING` | `true` | Rotate automatically when `X-Token-Rotation-Warning` is received |
| `ROTATE_ON_REQUIRED` | `true` | Rotate automatically when `X-Token-Rotation-Required` is received |

Set either to `false` to suppress automatic rotation and handle it manually instead.
With both defaults in place, tokens rotate silently as they age — no operator intervention
required under normal circumstances.

---

## Lockout and recovery

When a client reaches `TOKEN_LOCKOUT_DAYS`, every API request returns 403 until an operator
intervenes. To recover a locked client:

1. Open the **Status** dashboard in the admin under **Client Management**.
2. Click **Unlock Client** on the locked row.

This sets the lockout override and the rotation-required flag. On the client's next successful
API call, `X-Token-Rotation-Required` is sent and `ophix-client-core` rotates the token
automatically. Normal operation resumes without any manual token handling.

Clients that have never rotated (`last_token_rotation` is null) are not subject to lockout.

---

## Requirements

- `ophix-server-base >= 2026.06.08.01`
