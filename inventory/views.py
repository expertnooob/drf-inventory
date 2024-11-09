from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Category, Supplier, Product, Customer, Order, OrderItem, OrderStatus
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, SupplierSerializer, ProductSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer, OrderStatusSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        items_data = data.pop('items', [])

        order_serializer = self.get_serializer(data=data)
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()

        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product'])
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product with ID {item_data['product']} does not exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if product.quantity < item_data['quantity']:
                return Response(
                    {"error": f"Insuffent stock for product: {product.name}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            product.quantity -= item_data['quantity']
            product.save()

            OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'], price=item_data['price'])

        response_data = self.get_serializer(order).data
        return Response(response_data, status=status.HTTP_201_CREATED)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [IsAuthenticated]