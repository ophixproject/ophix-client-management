---
title: Client Management
slug: client-management
order: 520
section: Extensions
---

# Client Management

The Client Management plugin tracks API token age across the fleet and enforces a configurable rotation schedule. It adds a dedicated **Status** dashboard to the admin interface showing the rotation status of every registered client, along with client version information.

## How It Works

Every time a client makes an authenticated API request, the middleware records when its token was last rotated. Three age thresholds drive the escalating response:

| Threshold | Default | Effect |
|---|---|---|
| `TOKEN_WARN_DAYS` | 30 | Client row turns amber in the dashboard |
| `TOKEN_REQUIRE_DAYS` | 90 | Client is flagged; next request receives `X-Token-Rotation-Required: true` header |
| `TOKEN_LOCKOUT_DAYS` | 180 | Client is locked out and cannot authenticate until unlocked by an operator |

Set these in `.env` to tune for your environment. Setting `TOKEN_LOCKOUT_DAYS` to `0` disables lockout.

## Token States

| State | Meaning |
|---|---|
| OK | Token age is within the warn threshold |
| Warning | Token age has passed `TOKEN_WARN_DAYS` |
| Rotation Required | Token age has passed `TOKEN_REQUIRE_DAYS`; client will receive a rotation prompt |
| Requested by Operator | Operator has manually flagged this client for rotation |
| Locked | Token age has passed `TOKEN_LOCKOUT_DAYS`; client cannot authenticate |
| Never Rotated | No rotation has ever been recorded for this client |

## The Status Dashboard

The Status dashboard is linked from the **Client Management** section of the admin sidebar. It shows one row per client with:

- **Age bar** — visual representation of token age relative to the lockout (or require) threshold
- **Age in days** — exact number of days since last rotation
- **State badge** — colour-coded current state
- **Client version** — the version reported by the client on its last request (if available)

### Actions

Each client row has action buttons depending on its state:

- **Request rotation** — sets the rotation flag; the client will be prompted on its next request
- **Clear rotation** — removes a pending rotation request without rotating
- **Unlock** — resets a locked-out client; sets `last_token_rotation` to now and flags for immediate rotation

The **Request all overdue** button at the top flags every client that has passed `TOKEN_REQUIRE_DAYS` in a single action.

## Client Version Tracking

Clients that send the `X-Ophix-Client-Package` and `X-*-Client-Version` headers have their installed version recorded automatically on each request. No client-side configuration is required — Tier 1 clients built on `ophix-client-core` send these headers by default.

### Checking for Updates

Run the following command to query the configured pip index and record the latest available version for each registered client package:

```bash
ophix-manage check_client_updates
ophix-manage check_client_updates --quiet   # suppress table output
```

The results appear in the **Client Versions** summary panel on the Status dashboard, where each version entry is colour-coded as current or outdated.

Schedule this command to run daily via cron or an ophix-tasks scheduled task to keep the version data fresh.

## Installation

```bash
pip install ophix-client-management
ophix-manage migrate
```

Add to `.env` if you want non-default thresholds:

```
TOKEN_WARN_DAYS=30
TOKEN_REQUIRE_DAYS=90
TOKEN_LOCKOUT_DAYS=180
```

The Status dashboard link appears automatically in the admin sidebar under **Client Management** once the plugin is installed.
