from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import productCreateView, productListView, productDetailView
urlpatterns = [
    path('create/', productCreateView.as_view(), name='create'),
    path('list/', productListView.as_view(), name='list'),
    path('details/<slug:slug>/', productDetailView.as_view(), name='detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)