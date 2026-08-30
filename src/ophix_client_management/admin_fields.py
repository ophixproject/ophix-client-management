from django.utils.formats import date_format
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _, ngettext

from ophix_client_management.policy import token_state, STATE_LABELS

_STATE_STYLES = {
    "ok":        "color: var(--admin-interface-success-color)",
    "warn":      "color: var(--admin-interface-warning-color)",
    "require":   "color: var(--admin-interface-alert-color)",
    "locked":    "color: var(--admin-interface-alert-color); font-weight: bold",
    "unlocked":  "color: var(--admin-interface-warning-color); font-weight: bold",
    "never":     "color: var(--body-quiet-color)",
    "requested": "color: var(--admin-interface-warning-color); font-weight: bold",
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
            '{}&nbsp;&nbsp;<span style="{}">{}{}</span>',
            date_str, style, label, age_str,
        )
    return format_html('<span style="{}">{}</span>', style, label)


token_rotation_display.short_description = _("Last token rotation")
