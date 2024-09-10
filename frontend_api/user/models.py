from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from utils.models import DatesMixin


# Create your models here.
class User(AbstractBaseUser, DatesMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)