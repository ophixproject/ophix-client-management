from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin, messages
from django.db.models import Count
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from ophix.core.models import Client
from ophix_client_management.models import ClientVersion, ClientPackageVersion
from ophix_client_management.policy import get_thresholds, token_state, STATE_LABELS


@staff_member_required
def client_management_view(request):
    warn_days, require_days, lockout_days = get_thresholds()

    clients = Client.objects.filter(enabled=True).select_related("host", "version_record").order_by("host__name", "name")
    latest_versions = {
        r.pip_package: r.latest_version
        for r in ClientPackageVersion.objects.all()
    }
    bar_ref = lockout_days if lockout_days > 0 else require_days
    now = timezone.now()
    rows = []
    for client in clients:
        state, age_days = token_state(client)
        display_age = (now - client.last_token_rotation).days if client.last_token_rotation else None
        bar_age = age_days if age_days is not None else display_age
        if bar_age is not None:
            bar_pct = min(int(bar_age / max(bar_ref, 1) * 100), 100)
        else:
            bar_pct = 100  # never rotated: show as fully overdue
        version_record = getattr(client, "version_record", None)
        version_state = None
        if version_record and version_record.pip_package:
            latest = latest_versions.get(version_record.pip_package)
            if latest:
                version_state = "current" if version_record.version == latest else "outdated"
        rows.append({
            "client": client,
            "state": state,
            "label": STATE_LABELS[state],
            "age_days": display_age,
            "bar_pct": bar_pct,
            "client_version": version_record.version if version_record else None,
            "version_state": version_state,
        })

    # Version summary: group by (pip_package, version), annotate with client count.
    raw_summary = (
        ClientVersion.objects
        .filter(client__enabled=True)
        .exclude(pip_package="")
        .values("pip_package", "version")
        .annotate(count=Count("client_id"))
        .order_by("pip_package", "version")
    )
    version_summary = []
    current_pkg = None
    for entry in raw_summary:
        pkg = entry["pip_package"]
        latest = latest_versions.get(pkg)
        if pkg != current_pkg:
            version_summary.append({"package": pkg, "latest": latest, "rows": []})
            current_pkg = pkg
        if latest:
            state = "current" if entry["version"] == latest else "outdated"
        else:
            state = None
        version_summary[-1]["rows"].append({
            "version": entry["version"],
            "count": entry["count"],
            "state": state,
        })

    context = {
        **admin.site.each_context(request),
        "title": "Status",
        "rows": rows,
        "version_summary": version_summary,
        "warn_days": warn_days,
        "require_days": require_days,
        "lockout_days": lockout_days,
        "opts": {"app_label": "ophix_client_management"},
    }
    return TemplateResponse(request, "admin/ophix_client_management/client_management.html", context)


@staff_member_required
@require_POST
def request_rotation(request, client_id):
    Client.objects.filter(pk=client_id).update(rotation_required=True)
    return redirect("client_management")


@staff_member_required
@require_POST
def clear_rotation(request, client_id):
    Client.objects.filter(pk=client_id).update(rotation_required=False, lockout_override=False)
    return redirect("client_management")


@staff_member_required
@require_POST
def request_all_overdue(request):
    from datetime import timedelta
    _, require_days, _ = get_thresholds()
    cutoff = timezone.now() - timedelta(days=require_days)
    updated = Client.objects.filter(
        rotation_required=False,
        last_token_rotation__lt=cutoff,
    ).update(rotation_required=True)
    updated += Client.objects.filter(
        rotation_required=False,
        last_token_rotation__isnull=True,
    ).update(rotation_required=True)
    if updated:
        messages.success(request, f"{updated} client{'s' if updated != 1 else ''} flagged for rotation.")
    else:
        messages.info(request, "No overdue clients found.")
    return redirect("client_management")


@staff_member_required
@require_POST
def unlock_client(request, client_id):
    """Grant a locked-out client a restricted authentication bypass.

    Sets lockout_override so the client can authenticate to /api/client/self/
    endpoints (info, update, rotate-token) despite exceeding the lockout threshold.
    Domain artifact endpoints remain blocked until the client completes a real
    token rotation. Sets rotation_required so the client receives the
    X-Token-Rotation-Required header on its next request.
    last_token_rotation is left untouched — the token age remains accurate.
    Both flags are cleared by a successful token rotation.
    """
    Client.objects.filter(pk=client_id).update(
        lockout_override=True,
        rotation_required=True,
    )
    return redirect("client_management")
