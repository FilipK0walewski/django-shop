import datetime

from django.db import models


class Product(models.Model):

    def __str__(self):
        return self.product_id

    # class Meta:
    #     db_table = 'products'

    manufacturer = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50)
    ean = models.CharField(max_length=13)
    quantity = models.IntegerField()
    description = models.TextField()
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    price = models.FloatField()
    tax_rate = models.IntegerField()
    product_category_tree = models.CharField(max_length=255)
    color = models.CharField(max_length=50, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Image(models.Model):

    def __str__(self):
        return self.url

    url = models.CharField(50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    