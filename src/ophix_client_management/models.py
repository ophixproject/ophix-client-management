import re

from django.db import models
from django.utils.translation import gettext_lazy as _

_VERSION_HEADER_RE = re.compile(r"^X-\w+-Client-Version$", re.IGNORECASE)

_PACKAGE_HEADER = "X-Ophix-Client-Package"


def extract_client_version(headers):
    """Return the first X-*-Client-Version header value found, or None."""
    for name, value in headers.items():
        if _VERSION_HEADER_RE.match(name) and value:
            return value.strip()
    return None


def extract_client_package(headers):
    """Return the X-Ophix-Client-Package header value, or None."""
    value = headers.get(_PACKAGE_HEADER, "").strip()
    return value.lower() if value else None


class ClientVersion(models.Model):
    client = models.OneToOneField(
        "ophix_core.Client",
        on_delete=models.CASCADE,
        related_name="version_record",
    )
    version = models.CharField(max_length=100)
    pip_package = models.CharField(max_length=200, blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "ophix_client_management"
        verbose_name = _("Status")
        verbose_name_plural = _("Status")

    def __str__(self):
        return "{} — {}".format(self.client, self.version)


class ClientPackageVersion(models.Model):
    """Latest known version of a client pip package, populated by check_client_updates."""
    pip_package = models.CharField(max_length=200, unique=True)
    latest_version = models.CharField(max_length=100)
    checked_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "ophix_client_management"
        verbose_name = _("Client Package Version")
        verbose_name_plural = _("Client Package Versions")

    def __str__(self):
        return "{} {}".format(self.pip_package, self.latest_version)
