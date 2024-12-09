from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    google_id = models.CharField(max_length=255, unique=True, null=True)
    picture = models.URLField(null=True)