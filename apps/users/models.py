from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class MyUser(AbstractUser):
    mobile = models.CharField(max_length=100)
    check_review = models.BooleanField(default=False)

    def __str__(self):
        return self.username

