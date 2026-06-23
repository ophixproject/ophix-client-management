from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from ophix_client_management.models import ClientVersion


if getattr(settings, "SHOW_CLIENT_MANAGEMENT_MODEL", True):

    @admin.register(ClientVersion)
    class ClientVersionAdmin(admin.ModelAdmin):
        menu_order = 100

        def has_add_permission(self, request):
            return False

        def changelist_view(self, request, extra_context=None):
            return HttpResponseRedirect(reverse("client_management"))
