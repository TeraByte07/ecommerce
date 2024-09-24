from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('verify-payment/<str:reference>/', views.verify_payment, name='verify-payment'),
    path('add/shipping_address/', views.ShippingAddressCreateView.as_view(), name='add-shipping-address'),
    path('list/shipping_address/', views.ShippingAddressListView.as_view(), name='shipping-address-lists'),
    path('shipping_address/<int:pk>/', views.ShippingAddressDetailView.as_view(), name='shipping-address-details'),
]

