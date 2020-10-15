from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save



class Country(models.Model):
    name= models.CharField( max_length=50, blank=False, null=False)
    flag =models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Atrocity(models.Model):
    title = models.CharField(max_length=30, blank=False, null=False)
    region = models.CharField(max_length=30, blank=False, null=False)
    info= models.TextField()
    image_url = models.TextField()
    category = models.ManyToManyField('Category', related_name='Atrocity')
    country = models.ForeignKey(Country, on_delete=models.CASCADE,blank=True, null=True )
    slug = models.SlugField(unique = True) 
    featured= models.BooleanField(blank=True, null=True)
    date_added= models.DateTimeField( auto_now_add=True)
    videoURL= models.URLField( max_length=200)

    

    def __str__(self):
        return self.title
    def slug(self):
        return slugify(self.title)        



class Shirt(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    price = models.FloatField()
    shirt_type = models.CharField(max_length=30, blank=False, null=False) 
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    shirt_image = models.CharField( max_length=100)
    original_image = models.CharField(max_length =100)
    Atrocity = models.ManyToManyField(Atrocity, related_name='Shirt', blank=True)
    slug = models.SlugField(unique = True, null=True, blank=True)
    featured = models.BooleanField(blank=True, null=True)
    date_added= models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return self.name

  
    
    def get_absolute_url(self):
        return reverse("Alt:shirts", kwargs={"slug": self.slug})

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug='SLUG'

pre_save.connect(slug_generator, sender=Shirt)    
    



class Category(models.Model):
    name = models.CharField(max_length = 50, blank=False, )
    image = models.CharField(max_length=50)
    information =models.TextField()
    shirtList = models.ManyToManyField("Shirt", related_name='Category', blank=True, )
    nonProfitList = models.ManyToManyField("NonProfit", related_name='Category', blank=True, )

    def __str__(self):
        return self.name
    
 


class NonProfit(models.Model):
    name= models.CharField(max_length=50, blank=False, null=False)
    logo =  models.TextField()
    description =models.TextField()
    year_started = models.IntegerField()
    mission_statement=models.TextField()
    vision_statement=models.TextField()
    website_url= models.URLField()
    category = models.ManyToManyField(Category, related_name='NonProfit')
    slug = models.SlugField(unique = True)
    featured = models.BooleanField(blank=True, null=True)
    date_added= models.DateTimeField(auto_now_add=True)
    atrocity = models.ManyToManyField(Atrocity, blank=True, null=True, related_name='NonProfit')
    shirtList=models.ManyToManyField("Shirt",related_name='NonProfit' )
    main_image= models.CharField(max_length=100)




    def __str__(self):
        return self.name

    



