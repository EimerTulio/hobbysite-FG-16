from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    email = models.EmailField()
    nickname = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )

    def __str__(self):
        return self.name
