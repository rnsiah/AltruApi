from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import segno
import qrcode
from PIL import Image, ImageDraw
from django.core.files import File
import os   
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile






class User(AbstractUser):
    username = models.CharField(max_length=100, blank = True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)






def upload_path_handler():
    return None



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=5)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=50, null= True)
    city = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=5, null=True)
    qr_code= models.CharField(max_length=50, blank=True, null=True)
    shirt_list = models.ManyToManyField("Alt.Shirt", verbose_name=("shirts"), blank=True, related_name='UserProfiles')
    atrocity_list = models.ManyToManyField('Alt.Atrocity', blank=True, related_name='UserProfiles')
    nonProfit_list = models.ManyToManyField('Alt.NonProfit',  blank=True, related_name='UserProfiles')
    slug = models.SlugField(blank = True)
    qr_code_img = models.ImageField(upload_to= 'qr_codes', blank=True, null=True)


    def get_absolute_url(self):
        return reverse("api:user", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.user.email


    def get_userName(self):
        return str(self.username)

    def get_webUrl(self):
        user_site = f' www.altrueglobal/user/{self.get_userName()}' 
        return str(user_site)

    def save(self, *args, **kwargs):
        self.slug = self.username
        self.generate_qr()
        super(UserProfile, self).save()
        
    def generate_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(f'www.altrueglobal.org/true/{self.get_userName()}')
        qr.make(fit =True)
        filename = 'qr-%s.png' % (self.get_userName())
        img= qr.make_image()
        img.save(settings.MEDIA_ROOT + filename)
        with open (settings.MEDIA_ROOT +filename, "rb") as reopen:
            django_file= File(reopen)
            self.qr_code_img.save(filename, django_file, save=False)

    

class Balance(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    balance = models.IntegerField(default = 0)


    class Meta:
        verbose_name = _("Balance")
        verbose_name_plural = _("Balances")

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("Balance_detail", kwargs={"pk": self.pk})

        

        

class Donater(models.Model):
    email = models.EmailField(max_length=254)
    first_name = models.CharField( max_length=50)
    last_name = models.CharField(max_length = 50)
    amount = models.FloatField(default=0)
    sent_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.email
    





            
        
     
  



@receiver(post_save, sender=User)
def create_userProfile(sender, instance, created=False, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user = instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) 
            