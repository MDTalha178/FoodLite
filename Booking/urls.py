
from django.urls.conf import path
from . import views

urlpatterns = [
    path('create-booking', views.create_booking_view, name='create_booking'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]