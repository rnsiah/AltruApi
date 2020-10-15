from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    qr_code= models.CharField(max_length=50, blank=True, null=True)
    shirt_list = models.ManyToManyField("Alt.Shirt", verbose_name=("shirts"), blank=True, related_name='UserProfiles')
    atrocity_list = models.ManyToManyField('Alt.Atrocity', blank=True, related_name='UserProfiles')
    nonProfit_list = models.ManyToManyField('Alt.NonProfit',  blank=True, related_name='UserProfiles')
