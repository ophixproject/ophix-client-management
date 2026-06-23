from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_thresholds():
    return (
        getattr(settings, "TOKEN_WARN_DAYS", 30),
        getattr(settings, "TOKEN_REQUIRE_DAYS", 90),
        getattr(settings, "TOKEN_LOCKOUT_DAYS", 180),
    )


def token_state(client):
    """Return (state, age_days) for a client.

    States: ok, warn, require, locked, unlocked, never, requested.
    Lockout takes priority over rotation_required so the dashboard
    always shows the action that unblocks the client.
    """
    if client.rotation_required and client.last_token_rotation is None:
        return "requested", None

    if client.last_token_rotation is None:
        return "never", None

    warn_days, require_days, lockout_days = get_thresholds()
    age = (timezone.now() - client.last_token_rotation).days

    if lockout_days > 0 and lockout_days >= require_days and age >= lockout_days:
        if getattr(client, "lockout_override", False):
            return "unlocked", age  # Operator bypassed lockout; rotation still pending.
        return "locked", age
    if client.rotation_required:
        return "requested", None
    if age >= require_days:
        return "require", age
    if age >= warn_days:
        return "warn", age
    return "ok", age


STATE_LABELS = {
    "ok":        _("OK"),
    "warn":      _("Warning"),
    "require":   _("Rotation Required"),
    "locked":    _("Locked"),
    "unlocked":  _("Unlocked — Rotation Required"),
    "never":     _("Never Rotated"),
    "requested": _("Requested by Operator"),
}
