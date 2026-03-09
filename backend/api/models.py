from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_users',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_users',
        blank=True
    )

    def __str__(self):
        return self.email


class EyeTestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    original = models.URLField()
    left_eye = models.URLField(null=True, blank=True)
    right_eye = models.URLField(null=True, blank=True)
    has_leukocoria_left = models.BooleanField(null=True)
    has_leukocoria_right = models.BooleanField(null=True)

    def __str__(self):
        return f"Test by {self.user.email} on {self.created_at}"
