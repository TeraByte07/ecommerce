from django.urls import path
from .views import CartCreateView, CartListView, CartDetailView,CartItemCreateView, CartItemListView, CartItemDetailView

urlpatterns = [
    path('create/', CartCreateView.as_view(), name='cart-create'),
    path('lists/', CartListView.as_view(), name='cart-lists'),
    path('details/<int:pk>/', CartDetailView.as_view(), name='cart-details'),
    path('create/items/', CartItemCreateView.as_view(), name='cart-items-create'),
    path('lists/items/', CartItemListView.as_view(), name='cart-items-lists'),
    path('items/details/<int:pk>/', CartItemDetailView.as_view(), name='cart-items-details'),
]
