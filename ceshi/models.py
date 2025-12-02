# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

