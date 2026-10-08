plugin_category = "addon"
plugin_sort = 200

default_app_config = "ophix_client_management.apps.OphixClientManagementConfig"


def get_doc_tokens():
    """
    Optional hook discovered by ophix-docs (if installed), for {{ token }}
    substitution in shared markdown. Contributes a self-gating link pair:
    these tokens are only ever substituted when this plugin is actually
    installed (ophix-docs only discovers get_doc_tokens() hooks from
    installed plugins), so authoring `{{ cm_link_open }}ophix-client-management
    {{ cm_link_close }}` elsewhere always degrades to plain text when this
    plugin is absent, and becomes a real link to this package's own doc page
    (guaranteed to exist, since it ships in this same package) when present.
    """
    return {
        "cm_link_open": "[",
        "cm_link_close": "](/admin/ophix_docs/docpage/crosslink/ophix_client_management/client-management/)",
    }
