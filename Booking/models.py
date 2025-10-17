from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('started', 'Started'),
        ('reached', 'Reached'),
        ('collected', 'Collected'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    ASSIGNED_BY_CHOICES = [
        ('admin', 'Admin'),
        ('partner', 'Delivery Partner'),
        ('system', 'System Auto Assign'),
        ('none', 'Not Assigned'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    delivery_partner = models.ForeignKey(
        'DeliveryPartner.DeliveryPartner',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_bookings'
    )
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    food_details = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    assigned_by = models.CharField(
        max_length=20, choices=ASSIGNED_BY_CHOICES, default='none'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} ({self.customer.username})"

    @property
    def is_assigned(self):
        return self.delivery_partner is not None

    def can_be_cancelled(self):
        """
        Return True if the booking can be cancelled.
        """
        return self.status in ['pending', 'assigned', 'started']
