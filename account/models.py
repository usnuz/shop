from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    status = models.IntegerField(choices=(
        (1, 'admin'),
        (2, 'moderator'),
        (3, 'client'),
    ), blank=True, null=True)
    avatar = models.ImageField(upload_to='usrpic/', null=True, blank=True)

    class Mete(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class BillingDetails(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.tel
