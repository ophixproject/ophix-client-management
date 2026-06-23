from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OphixClientManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ophix_client_management"
    verbose_name = _("Client Management")
    admin_order = 500

    def ready(self):
        from ophix.core.admin import ClientAdmin
        from ophix_client_management.columns import token_status_column
        ClientAdmin.register_column(token_status_column, before_domain=True)
