import datetime

from django.db import models
from django.contrib.auth.models import User


class CategoryManager(models.Manager):
    def get_category_tree(self):

        def get_children(parent_id):
            children = self.filter(parent_id=parent_id)
            if not children:
                return None

            childrens = []
            for i in children:
                tmp = get_children(i.id)
                childrens.append({'id': i.id, 'name': i.name, 'children': tmp})

            return childrens

        tree = []
        for i in self.filter(parent_id__isnull=True):
            children = get_children(i.id)
            tree.append({'id': i.id, 'name': i.name, 'children': children})

        return tree

    def get_subcategories(self, category_id):
        subcategories = [category_id]

        queue = [category_id]
        while queue:
            parent_id = queue.pop(0)
            sub = self.filter(parent_id=parent_id)
            for i in sub:
                queue.append(i.id)
                subcategories.append(i.id)

        return subcategories


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    objects = CategoryManager()

    def __str__(self):
        return self.name


class Product(models.Model):

    def __str__(self):
        return self.product_id

    manufacturer = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50, unique=True)
    ean = models.CharField(max_length=13)
    quantity = models.IntegerField()
    description = models.TextField()
    name = models.CharField(max_length=255)
    price = models.FloatField()
    tax_rate = models.IntegerField()
    color = models.CharField(max_length=50, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class ProductComment(models.Model):

    text = models.CharField(max_length=255, default="Fajne.")    
    rating = models.IntegerField(default=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):

    def __str__(self):
        return self.url

    url = models.CharField(50, unique=True)
    downloaded = models.ImageField(upload_to='images/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    order_id = models.UUIDField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderItem(models.Model):
    price = models.FloatField()
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Delivery(models.Model):
    email = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=6)
    phone = models.CharField(max_length=12)
    company = models.CharField(max_length=50, null=True, blank=True)
    nip = models.IntegerField(null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Transaction(models.Model):
    transaction_id = models.UUIDField()
    amount = models.FloatField()
    payment_method = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
