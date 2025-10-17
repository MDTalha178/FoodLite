from os import name
from django.urls.conf import path
from . import views

# urls.py
urlpatterns = [
    path('partner-dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('accept-booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('update-booking-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
]

