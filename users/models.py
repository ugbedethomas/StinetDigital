from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('TRAINER', 'Trainer'),
        ('CLIENT', 'Client'),
        ('ADMIN', 'Admin'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='STUDENT'
    )

    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username