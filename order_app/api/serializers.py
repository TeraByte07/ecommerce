from rest_framework import serializers
from order_app.models import Order, ShippingAddress

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'postal_code', 'country']

class OrderSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressSerializer(write_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'shipping_address', 'status', 'created_at', 'updated_at', 'total_amount']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_amount']

    def create(self, validated_data):
        # Extract shipping address data from the validated data
        shipping_address_data = validated_data.pop('shipping_address')
        user = self.context['request'].user

        # Create or get the existing shipping address for the user
        shipping_address, created = ShippingAddress.objects.get_or_create(user=user, **shipping_address_data)

        # Create the order using the provided data
        order = Order.objects.create(user=user, shipping_address=shipping_address, **validated_data)
        return order

    def update(self, instance, validated_data):
        shipping_address_data = validated_data.pop('shipping_address', None)
        # Update the shipping address if data is provided
        if shipping_address_data:
            ShippingAddress.objects.filter(id=instance.shipping_address.id).update(**shipping_address_data)
        # Update the order instance
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
