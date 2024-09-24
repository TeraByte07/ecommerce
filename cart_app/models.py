from django.db import models
from django.contrib.auth.models import User
from product_app.models import product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def total_price(self):
        # Assuming you have a `CartItem` model related to `Cart`
        return sum(item.total_price() for item in self.items.all())
        
    
    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(default=1)
    
    def total_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart"
