import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from squash_club import settings


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return f"Profil użytkownika {self.user.username}"

    class Meta:
        verbose_name = "profil"
        verbose_name_plural = "Profile"

    def clean(self):
        pattern = r'^\d{3} *\d{3} *\d{3}$'
        if not re.fullmatch(pattern, self.phone_number):
            raise ValidationError("Nieprawidłowy numer telefonu. Podaj numer w formacie: 111 111 111")