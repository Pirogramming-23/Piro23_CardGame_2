from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    user_score = models.IntegerField(default=0)

    def __str__(self):
        return self.username