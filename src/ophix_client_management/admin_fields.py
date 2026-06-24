from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

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
    age_str = " ({} {})".format(age_days, _("days")) if age_days is not None else ""
    date_str = obj.last_token_rotation.strftime("%Y-%m-%d %H:%M") if obj.last_token_rotation else None
    if date_str:
        return format_html(
            '<span style="{}">{}{}</span>'
            '<br><span style="font-size:0.85em;color:var(--body-quiet-color);margin-top:2px;display:inline-block">{}</span>',
            style, label, age_str, date_str,
        )
    return format_html('<span style="{}">{}</span>', style, label)


token_rotation_display.short_description = _("Last token rotation")
