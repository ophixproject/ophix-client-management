from django.urls import path
from ophix_client_management import views

urlpatterns = [
    path("client-management/", views.client_management_view, name="client_management"),
    path("client-management/request/<int:client_id>/", views.request_rotation, name="client_management_request"),
    path("client-management/clear/<int:client_id>/", views.clear_rotation, name="client_management_clear"),
    path("client-management/unlock/<int:client_id>/", views.unlock_client, name="client_management_unlock"),
    path("client-management/request-all-overdue/", views.request_all_overdue, name="client_management_request_all_overdue"),
]
