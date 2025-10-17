from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.conf import settings

from Booking.models import Booking
from Utils.models import BaseModel


# models.py
class DeliveryPartner(BaseModel):
    STATUS_CHOICES = [
        ('offline', 'Offline'),
        ('online', 'Online'),
        ('available', 'Available'),
        ('busy', 'Busy'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='delivery_partner_profile'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    current_booking = models.ForeignKey(
        Booking, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='current_delivery_partner'
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"

