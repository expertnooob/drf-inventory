from django.db import transaction
from rest_framework import viewsets
from .models import Category, Supplier, Product, Customer, Order, OrderItem
from .serializers import (
    CategorySerializer, SupplierSerializer, ProductSerializer,
    CustomerSerializer, OrderSerializer, OrderItemSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'supplier').all()
    serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('order_items__product').all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order', 'product').all()
    serializer_class = OrderItemSerializer