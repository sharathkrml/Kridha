
from django.urls import path
from .views import home, category, product, search
urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('category/<slug>/', category, name='category'),
    path('category/', category, name='category_url'),
    path('product/<slug>/', product, name='product'),
    path('product/', product, name='product_url'),
]
