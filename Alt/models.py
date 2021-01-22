from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from api.models import UserProfile, User
from django.core.validators import MinValueValidator, MaxValueValidator


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

    def get_absolute_url(self):
        return reverse ('Alt:Atrocity', kwargs={'slug':self.slug})




class Shirt(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    price = models.FloatField()
    discount_price = models.FloatField()
    shirt_type = models.CharField(max_length=30, blank=False, null=False) 
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    shirt_image = models.CharField( max_length=100)
    original_image = models.CharField(max_length =100)
    Atrocity = models.ManyToManyField(Atrocity, related_name='Shirt', blank=True)
    slug = models.SlugField(unique = True, null=True, blank=True)
    featured = models.BooleanField(blank=True, null=True)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

    def addToCart(self):
        return reverse('core: add-to-cart', kwargs={
            'slug':self.slug
        })

    
    def removeFromCart(self):
        return reverse( 'core: remove-from-cart', kwargs={
            'slug':self.slug
        })


    def get_absolute_url(self):
        return reverse("Alt:shirts", kwargs={"slug": self.slug})

    def no_of_ratings(self):
        ratings = Rating.objects.filter(shirt =self)
        return len(ratings)

    def average_rating(self):
        sum = 0
        ratings = Rating.objects.filter(shirt =self)
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            return sum /len(ratings)
        else:
            return 0


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug='SLUG'

pre_save.connect(slug_generator, sender=Shirt)    
    
class Rating(models.Model):
    shirt = models.ForeignKey("Alt.Shirt", on_delete=models.CASCADE)
    user = models.ForeignKey("api.User", on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'shirt'),)
        index_together = (('user', 'shirt'),)


    def __str__(self):
        return self.shirt.name

    def get_absolute_url(self):
        return reverse("Rating_detail", kwargs={"pk": self.pk})


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
    

    def get_absolute_url(self):
        return reverse("Alt:NonProfit", kwargs={"slug": self.slug})
    



    def __str__(self):
        return self.name

    
class OrderItem(models.Model):
    user = models.ForeignKey("api.UserProfile", on_delete=models.CASCADE)
    ordered_shirt = models.ForeignKey("Alt.Shirt", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    
    def __str__(self):
        return f'{self.quantity} of {self.ordered_shirt.name}'


    def get_total_shirt_price(self):
        return self.quantity * self.ordered_shirt.price

    def get_discount_shirt_price(self):
        return self.quantity * self.ordered_shirt.discount_price

    def get_amount_donated(self):
        return self.get_total_shirt_price() * .35

    def get_final_price(self):
        if self.ordered_shirt.discount_price:
            return self.get_discount_shirt_price()
        return self.get_total_shirt_price()


class Order(models.Model):
    user = models.ForeignKey("api.UserProfile", on_delete=models.CASCADE)
    shirts = models.ManyToManyField("Alt.OrderItem")
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    completed = models.BooleanField(default = False)

    def __str__(self):
        return self.user.email

    def get_total_price(self):
        total = 0
        for order_item in self.shirts.all():
            total += OrderItem.get_final_price()
        return total



class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email