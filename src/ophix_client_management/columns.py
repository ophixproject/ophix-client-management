from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from ophix_client_management.policy import token_state, STATE_LABELS

_STATE_STYLES = {
    "ok":        "color: var(--admin-interface-success-color); font-weight: 600",
    "warn":      "color: var(--admin-interface-warning-color); font-weight: 600",
    "require":   "color: var(--admin-interface-alert-color); font-weight: 600",
    "locked":    "color: var(--admin-interface-alert-color); font-weight: 600",
    "never":     "color: var(--admin-interface-muted-color); font-weight: 600",
    "requested": "color: var(--admin-interface-warning-color); font-weight: 600",
}


def token_status_column(self, obj):
    state, age_days = token_state(obj)
    label = STATE_LABELS[state]
    style = _STATE_STYLES[state]
    age_str = " ({} days)".format(age_days) if age_days is not None else ""
    return format_html('<span style="{}">{}{}</span>', style, label, age_str)


token_status_column.short_description = _("Token Status")
token_status_column.allow_tags = True
