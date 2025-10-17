from django.db import models
from django.utils import timezone

from Utils.models import UserBaseModel, BaseModel


class User(UserBaseModel):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('partner', 'Delivery Partner'),
        ('admin', 'Admin'),
    )
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'mobile'

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_customer(self):
        return self.role == 'customer'

    def is_delivery_partner(self):
        return self.role == 'partner'

    def is_admin_user(self):
        return self.role == 'admin' or self.is_staff

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']


class OTPVerification(BaseModel):
    mobile_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    attempts = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP for {self.mobile_number}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self):
        return not self.is_expired() and self.attempts < 3
