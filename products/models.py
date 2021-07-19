from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
# Create your models here.


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    productname = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, blank=True)
    sub_category = models.ForeignKey('Category', on_delete=models.CASCADE)
    stylist_notes = models.TextField(blank=True)
    selling_price = models.IntegerField(blank=True)
    discount = models.IntegerField(blank=True)
    image = models.CharField(max_length=2000, blank=True)
    additional_info = models.TextField(blank=True)
