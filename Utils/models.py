import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields for all models.

    Fields:
        created_at (DateTimeField): Timestamp when the object was created.
        updated_at (DateTimeField): Timestamp when the object was last updated.
        is_deleted (BooleanField): Flag for soft deletion.
                                   Instead of deleting records physically, mark them as deleted.
    Usage:
        Inherit this model in any Django model to get these fields automatically.
    """
    # UUID as primary key for improved security and data migration flexibility.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UserBaseModel(AbstractBaseUser, PermissionsMixin):
    """
    Abstract base user model that provides common user fields and authentication hooks.

    Fields:
        created_at (DateTimeField): Timestamp when user was created.
        updated_at (DateTimeField): Timestamp when user was last updated.
        is_deleted (BooleanField): Flag for soft deletion of users.
        last_login (DateTimeField): Last login timestamp (overrides AbstractBaseUser's default).
        is_active (BooleanField): Flag indicating if this user is active.
                                  Inactive users are treated as deleted in login checks.
        is_staff (BooleanField): Designates whether the user can access the admin site.

    Usage:
        Inherit this model when creating a custom User model (for example: `class User(UserBaseModel)`).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        abstract = True
