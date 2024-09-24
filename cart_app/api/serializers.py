from rest_framework import serializers
from cart_app.models import Cart,CartItem
from product_app.api.serializers import productSerializer

class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.StringRelatedField(read_only=True)
    product_details = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['cart', 'product_details', 'quantity']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        
        # Assuming you want to assign the cart of the current user
        cart = Cart.objects.get(user=user)

        product_instance = validated_data.get('product')
        quantity = validated_data.get('quantity')

        # Create cartItem with the correct user and cart
        cart_item = CartItem.objects.create(cart=cart, product=product_instance, quantity=quantity)

        return cart_item
    
    def get_product_details(self, obj):
        return {
            'name': obj.product.name,
            'price': obj.product.price  # Assuming price is a field in your product model
        }
    
class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True, read_only=True, source='items')
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Cart
        fields = ['user', 'created_at', 'cart_item']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Optional: Customize how cart_items are displayed or any other formatting
        return representation