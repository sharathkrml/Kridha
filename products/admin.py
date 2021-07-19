from django.contrib import admin
from .models import Category, Product
from mptt.admin import MPTTModelAdmin

# Register your models here.
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)
