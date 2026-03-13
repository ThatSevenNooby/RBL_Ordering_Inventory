from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)