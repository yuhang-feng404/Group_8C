from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    STUDENT = 'student'
    SOCIETY_ADMIN = 'society_admin'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (SOCIETY_ADMIN, 'Society Admin'),
    ]


    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)


    profile_picture = models.CharField(max_length=255, blank=True, null=True)


    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

