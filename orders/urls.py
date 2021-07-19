
from django.urls import path
from .views import addtocart, getcart, cart, checkout, address, getorder, wishlist
urlpatterns = [
    path('addtocart/', addtocart, name='addtocart'),
    path('getcart/', getcart, name='getcart'),
    path('cart/', cart, name='cart'),
    path('checkout_address/', address, name='checkout_address'),
    path('checkout/', checkout, name='checkout'),
    path('getorder/', getorder, name='getorder'),
    path('wishlist/', wishlist, name='wishlist'),
]
