from .serializers import OrderSerializer, ShippingAddressSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from cart_app.models import Cart
from order_app.models import Order, ShippingAddress
import requests
from django.conf import settings
from .permissions import IsAccountOwner
from rest_framework.permissions import IsAdminUser
from rest_framework import generics

import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAccountOwner])
def checkout(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)

    shipping_address_data = request.data.get('shipping_address')
    if shipping_address_data:
        shipping_address, created = ShippingAddress.objects.get_or_create(user=user, **shipping_address_data)
    else:
        return Response({"error": "Shipping address is required"}, status=400)

    existing_order = Order.objects.filter(cart=cart).first()
    if existing_order:
        return Response({"error": "An order for this cart already exists."}, status=400)

    total_amount = cart.total_price() * 100  # Convert to kobo
    logger.info(f"Total amount calculated: {total_amount}")

    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        "email": user.email,
        "amount": total_amount,
    }
    payment_response = requests.post(url, headers=headers, json=data)

    if payment_response.status_code == 200:
        payment_data = payment_response.json()
        payment_reference = payment_data['data']['reference']

        order = Order.objects.create(
            user=user,
            cart=cart,
            shipping_address=shipping_address,
            status="pending",
            payment_reference=payment_reference
        )
        logger.info(f"Order created with total amount: {order.total_amount}")
        order_serializer = OrderSerializer(order)

        return Response({
            "message": "Order created successfully, complete your payment",
            "payment_url": payment_data['data']['authorization_url'],
            "payment_reference": payment_reference,
            "order": order_serializer.data,
        })

    return Response(payment_response.json(), status=payment_response.status_code)





import logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAccountOwner])
def verify_payment(request, reference):
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['data']['status'] == 'success':
            order = get_object_or_404(Order, payment_reference=reference)
            order.status = "shipped"
            order.save()

            # Ensure the cart exists and is correctly referenced
            cart = order.cart
            if not cart.pk:
                return Response({"error": "Cart not found or has been deleted."}, status=400)
            
            try:
                for item in cart.items.all():
                    product = item.product
                    if product.stock >= item.quantity:
                        product.stock -= item.quantity
                        product.save()
                    else:
                        return Response({"error": f"Not enough stock for {item.product.name}"}, status=400)
                logger.info(f"Clearing items for cart {cart.id}")
                cart.items.all().delete() # Clear cart items after successful checkout

            except Exception as e:
                logger.error(f"Error during cart processing: {e}")
                return Response({"error": "Error during cart processing."}, status=500)

            order_serializer = OrderSerializer(order)

            return Response({
                "message": "Payment verified and order processed",
                "order": order_serializer.data
                #"total_amount": 
            })
    
    logger.error(f"Payment verification failed with response: {response.json()}")
    return Response({"error": "Payment verification failed"}, status=400)



class ShippingAddressCreateView(generics.CreateAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAccountOwner]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class ShippingAddressListView(generics.ListAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAdminUser]

class ShippingAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAccountOwner]
    
    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)
