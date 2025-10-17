
from django.urls.conf import path
from . import views

urlpatterns = [
    path('customer-dashboard', views.customer_dashboard_view, name='customer_dashboard'),
]