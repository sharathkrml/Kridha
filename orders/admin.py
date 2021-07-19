from django.contrib import admin
from .models import Cart, Order, Wishlist
# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wishlist)
