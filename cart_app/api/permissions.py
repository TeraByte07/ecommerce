from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from cart_app.models import Cart, CartItem
class CustomIsAuthenticated(IsAuthenticated):
    message = "You are not an authenticated user. Please log in to continue."

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return Response({"detail": self.message}, status=status.HTTP_401_UNAUTHORIZED)
        return is_authenticated

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the object is a CartItem
        if isinstance(obj, CartItem):
            return obj.cart.user == request.user or request.user.is_staff
        
        # Check if the object is a Cart
        if isinstance(obj, Cart):
            return obj.user == request.user or request.user.is_staff
        
        # If it’s neither CartItem nor Cart, return False by default
        return False
