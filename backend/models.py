from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

import os


# Create your models here.
class Tapper(models.Model):
    """
    Model to represent a TAPP User
    """
    user = models.OneToOneField(User)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=16)
    digest = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.id and not self.digest:
            self.digest = os.urandom(16).encode('hex')
        return super(Tapper, self).save(*args,**kwargs)
