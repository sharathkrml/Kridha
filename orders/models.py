from django.db import models
from django.db.models.base import Model
from products.models import Product
from accounts.models import CustomUser, Addresses
# Create your models here.


class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    cart_total_price = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.cart_total_price:
            self.cart_total_price = self.quantity * self.product_id.selling_price
        super(Cart, self).save(*args, **kwargs)


class Order(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_ids = models.ManyToManyField(Cart)
    address_id = models.ForeignKey(Addresses, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now=True)
    total_price = models.IntegerField()


class Wishlist(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
