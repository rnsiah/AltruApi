from django.contrib import admin
from .models import Shirt, Atrocity, Category, NonProfit, Country




class ShirtAdmin(admin.ModelAdmin):
    list_display =('name',)
    prepopulated_fields = {'slug': ('name',)} 

admin.site.register(Shirt, ShirtAdmin)


class NonProfitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)} 

admin.site.register(NonProfit, NonProfitAdmin)

# Register your models here.

admin.site.register(Atrocity)
admin.site.register(Category)

admin.site.register(Country)

    
