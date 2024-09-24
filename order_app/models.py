from django.db import models
from django.contrib.auth.models import User
from product_app.models import product 
from cart_app.models import Cart

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f"{self.address}, {self.city}, {self.country}"

class Order(models.Model):
    order_status_choices = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=25, choices=order_status_choices, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def save(self, *args, **kwargs):
        # Dynamically calculate total amount from the cart
        if not self.total_amount:
            self.total_amount = self.cart.total_price()  # Assuming total_price returns a Decimal
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
