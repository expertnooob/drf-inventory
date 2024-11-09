from django.contrib import admin
from inventory.models import Category, Supplier, Product, Customer, Order, OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

