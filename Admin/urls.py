# urls.py
from django.urls import path

from Admin import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('assign-partner/<int:booking_id>/', views.assign_partner, name='assign_partner'),
]
