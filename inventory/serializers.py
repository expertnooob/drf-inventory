from rest_framework import serializers
from .models import Category, Supplier, Product, Customer, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'supplier', 'description', 'quantity', 'price']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact', 'address']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'description']

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal']
        read_only_fields = ['subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'created_at', 'items']
        read_only_fields = ['id', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)  # Create the order

        for item_data in items_data:
            # Extract and remove the product key from item_data
            product = item_data.pop('product')

            # Validate stock
            if product.quantity < item_data['quantity']:
                raise serializers.ValidationError(
                    {"items": f"Insufficient stock for product: {product.name}"}
                )

            # Deduct stock and create OrderItem
            product.deduct_stock(item_data['quantity'])
            OrderItem.objects.create(order=order, product=product, **item_data)

        return order
