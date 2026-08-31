from django.utils.formats import date_format
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _, ngettext

from ophix_client_management.policy import token_state, STATE_LABELS

_STATE_STYLES = {
    "ok":        "color: var(--admin-interface-success-color); font-weight: 600",
    "warn":      "color: var(--admin-interface-warning-color); font-weight: 600",
    "require":   "color: var(--admin-interface-alert-color); font-weight: 600",
    "locked":    "color: var(--admin-interface-alert-color); font-weight: 600",
    "unlocked":  "color: var(--admin-interface-warning-color); font-weight: 600",
    "never":     "color: var(--body-quiet-color); font-weight: 600",
    "requested": "color: var(--admin-interface-warning-color); font-weight: 600",
}


def token_rotation_display(self, obj):
    state, age_days = token_state(obj)
    label = STATE_LABELS[state]
    style = _STATE_STYLES[state]
    age_str = " ({})".format(
        ngettext("%(count)d day", "%(count)d days", age_days) % {"count": age_days}
    ) if age_days is not None else ""
    if obj.last_token_rotation:
        # Same localized DATETIME_FORMAT rendering Django uses for this field
        # when ophix-client-management isn't installed, so the two cases read
        # identically aside from the appended status.
        date_str = date_format(obj.last_token_rotation, "DATETIME_FORMAT")
        return format_html(
            '{}<br><span style="{}">{}{}</span>',
            date_str, style, label, age_str,
        )
    return format_html('<span style="{}">{}</span>', style, label)


token_rotation_display.short_description = _("Last token rotation")
