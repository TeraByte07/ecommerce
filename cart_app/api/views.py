from .serializers import CartSerializer, CartItemSerializer
from cart_app.models import Cart, CartItem
from rest_framework import generics
from .permissions import IsAccountOwner, CustomIsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from product_app.models import product

class CartCreateView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CustomIsAuthenticated, IsAccountOwner]

    def create(self, request, *args, **kwargs):
        user = request.user
        
        # Check if a cart already exists for the user
        cart, created = Cart.objects.get_or_create(user=user)
        
        if not created:
            return Response({"error": "A cart already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        # If the cart is newly created, return the cart data
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAccountOwner]

class CartItemCreateView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    
    def perform_create(self, serializer):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)

        # Ensure the product is provided in the request data
        product_id = self.request.data.get('product')
        if not product_id:
            raise serializers.ValidationError({"error": "Product is required"})
        
        # Save cart item with the provided product and cart
        product_instance = product.objects.get(id=product_id)
        serializer.save(cart=cart, product=product_instance)

class CartItemListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    
    def get_queryset(self):
        # Return only the cart items belonging to the logged-in user's cart
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAccountOwner]

    def perform_update(self, serializer):
        user = self.request.user
        cart_item = self.get_object()  # Get the CartItem instance being updated

        # Ensure that the cart associated with the CartItem belongs to the user
        if cart_item.items.user != user:
            raise serializers.ValidationError("You do not have permission to update this cart item.")

        # Save the updated CartItem instance
        serializer.save()
