from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Product, Order, OrderItem, CheckoutLog
from .serializers import (
    ProductSerializer, OrderSerializer, OrderItemSerializer,
    CheckoutLogSerializer
)
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if OrderItem.objects.filter(product=product).exists():
            return Response(
                {'error': 'Cannot delete product that has already been ordered.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return orders belonging to the current user
        return Order.objects.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        # Ensure new orders are associated with the current user
        serializer.save(customer=self.request.user)

from rest_framework.permissions import IsAuthenticated, IsAdminUser

class AdminOrderListView(generics.ListAPIView):
    """View for admins to see all orders regardless of user"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]  # Only admin users can access this view
   
    def get_queryset(self):
        # Only staff/admin users should see all orders
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Order.objects.all()
        # Regular users should only see their own orders
        return Order.objects.filter(customer=self.request.user)


class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get the product and requested quantity from the serializer
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        
        # Check if the product has enough stock
        if product.stock < quantity:
            raise serializers.ValidationError("Not enough stock available.")
        
        # Get the current user's active cart (incomplete order)
        cart, created = Order.objects.get_or_create(
            customer=self.request.user,
            complete=False,
            defaults={'status': 'cart'}  # Add default status if you have a status field
        )
        
        # Check if this product is already in the cart
        existing_item = OrderItem.objects.filter(order=cart, product=product).first()
        
        if existing_item:
            # If the product is already in the cart, update the quantity
            existing_item.quantity += quantity
            existing_item.save()
            
            # Update product stock
            product.stock -= quantity
            product.save()
            
            # Return the updated order item
            return existing_item
        else:
            # Create new order item
            order_item = serializer.save(order=cart)
            
            # Update product stock
            product.stock -= quantity
            product.save()
            
            # Create checkout log only if it's a new cart
            if created:
                CheckoutLog.objects.create(
                    employee=self.request.user,
                    order=cart
                )
            
            return order_item

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_item = self.perform_create(serializer)
        
        # Use the serializer for the response
        response_serializer = self.get_serializer(order_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CompleteOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        # Get the current user's active cart
        try:
            cart = Order.objects.get(
                customer=request.user,
                complete=False
            )
        except Order.DoesNotExist:
            return Response(
                {"detail": "No active cart found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Mark the order as complete
        cart.complete = True
        if hasattr(cart, 'status'):
            cart.status = 'pending'  # or whatever status you use for completed orders
        cart.save()
        
        # Create checkout log if it doesn't exist yet
        if not CheckoutLog.objects.filter(order=cart).exists():
            CheckoutLog.objects.create(
                employee=request.user,
                order=cart
            )
        
        # Return the completed order
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CurrentCartView(generics.RetrieveAPIView):
    """View to get the current user's active cart"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        cart, created = Order.objects.get_or_create(
            customer=self.request.user,
            complete=False,
            defaults={'status': 'cart'} if hasattr(Order, 'status') else {}
        )
        return cart

class CheckoutLogListView(generics.ListAPIView):
    queryset = CheckoutLog.objects.all()
    serializer_class = CheckoutLogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_checked']

class CheckoutLogCreateView(generics.CreateAPIView):
    queryset = CheckoutLog.objects.all()
    serializer_class = CheckoutLogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'is_staff': request.user.is_staff
    })