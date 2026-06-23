from django.conf import settings
from django.utils import timezone

from ophix_client_management.models import ClientVersion, extract_client_version, extract_client_package


class TokenRotationSignalMiddleware:
    """
    Injects rotation signal headers into API responses:
      X-Token-Rotation-Required: true  — overdue, past require threshold, or operator-flagged
      X-Token-Rotation-Warning:  true  — approaching deadline (between warn and require thresholds)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self._maybe_signal(request, response)
        return response

    def _maybe_signal(self, request, response):
        if response.status_code != 200:
            return
        if not request.path.startswith("/api/"):
            return

        from ophix.core.models import Client
        client = request.user
        if not isinstance(client, Client):
            return

        version = extract_client_version(request.headers)
        package = extract_client_package(request.headers)
        if version or package:
            record, created = ClientVersion.objects.get_or_create(
                client=client,
                defaults={"version": version or "", "pip_package": package or ""},
            )
            if not created:
                update_fields = []
                if version and record.version != version:
                    record.version = version
                    update_fields += ["version", "updated_at"]
                if package and record.pip_package != package:
                    record.pip_package = package
                    update_fields.append("pip_package")
                if update_fields:
                    record.save(update_fields=update_fields)

        if client.rotation_required:
            response["X-Token-Rotation-Required"] = "true"
            return

        if client.last_token_rotation is None:
            return

        warn_days = getattr(settings, "TOKEN_WARN_DAYS", 30)
        require_days = getattr(settings, "TOKEN_REQUIRE_DAYS", 60)
        age = (timezone.now() - client.last_token_rotation).days

        if age >= require_days:
            response["X-Token-Rotation-Required"] = "true"
        elif age >= warn_days:
            response["X-Token-Rotation-Warning"] = "true"
