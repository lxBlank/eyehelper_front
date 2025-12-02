from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)
    list_filter = ('price',)

