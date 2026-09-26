"""
ophix-manage check_client_updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Check all known fleet client pip packages against the configured pip index
and update the ClientPackageVersion table with the latest available version.

Packages are discovered automatically from the pip_package field on
ClientVersion — no manual registration needed.  As new clients connect and
send X-*-Client-Package headers, they are picked up on the next run.

Run daily via cron or ophix-tasks scheduled task to keep the version data fresh:
    ophix-manage check_client_updates
    ophix-manage check_client_updates --quiet
"""

import re
import subprocess
import sys

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.translation import gettext as _


def _format_ophix_version(version: str) -> str:
    """Restore leading zeros stripped by PEP 440 normalisation (YYYY.MM.DD.NN)."""
    parts = version.split(".")
    if len(parts) == 4 and parts[0].isdigit() and len(parts[0]) == 4:
        try:
            year, month, day, seq = parts
            return f"{year}.{int(month):02d}.{int(day):02d}.{int(seq):02d}"
        except ValueError:
            pass
    return version


_INDEX_LINE_RE = re.compile(r"^(\S+)\s+\(([^)]+)\)", re.IGNORECASE)


def _get_latest_version(package_name: str, timeout: int) -> str | None:
    """Query the configured pip index for the latest version of a package."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "index", "versions", package_name],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    for line in result.stdout.splitlines():
        line = line.strip()
        m = _INDEX_LINE_RE.match(line)
        if m and m.group(1).lower() == package_name.lower():
            return _format_ophix_version(m.group(2))
    return None


class Command(BaseCommand):
    help = _("Check fleet client pip packages against the configured index for available updates.")

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=30,
            metavar="SECONDS",
            help=_("Pip query timeout per package in seconds (default: 30)."),
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help=_("Suppress table output. Results are still written to the database."),
        )

    def handle(self, *args, **options):
        from ophix_client_management.models import ClientVersion, ClientPackageVersion

        timeout = options["timeout"]
        quiet = options["quiet"]

        packages = sorted(
            ClientVersion.objects
            .exclude(pip_package="")
            .values_list("pip_package", flat=True)
            .distinct()
        )

        if not packages:
            if not quiet:
                self.stdout.write(_("No client packages registered yet. Clients must send the X-Ophix-Client-Package header."))
            return

        now = timezone.now()
        results = []

        for package in packages:
            if not quiet:
                self.stderr.write(f"  Checking {package}...\r", ending="")
                self.stderr.flush()
            latest = _get_latest_version(package, timeout)
            if latest:
                ClientPackageVersion.objects.update_or_create(
                    pip_package=package,
                    defaults={"latest_version": latest, "checked_at": now},
                )
            results.append((package, latest))

        if not quiet:
            self.stderr.write(" " * 60 + "\r", ending="")

            col_pkg = str(_("Package"))
            col_latest = str(_("Latest"))
            col_status = str(_("Status"))

            w_pkg = max(len(col_pkg), max(len(r[0]) for r in results))
            w_latest = max(len(col_latest), max(len(r[1]) if r[1] else 3 for r in results))

            self.stdout.write(f"{col_pkg:<{w_pkg}}  {col_latest:<{w_latest}}  {col_status}")
            self.stdout.write("  ".join(["-" * w_pkg, "-" * w_latest, "-" * len(col_status)]))

            for package, latest in results:
                if latest:
                    status = self.style.SUCCESS(str(_("OK")))
                    latest_display = latest
                else:
                    status = self.style.WARNING(str(_("Not found on index")))
                    latest_display = "—"
                self.stdout.write(f"{package:<{w_pkg}}  {latest_display:<{w_latest}}  {status}")
