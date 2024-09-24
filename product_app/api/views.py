from .serializers import productSerializer, categorySerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from product_app.models import product, Category
from .permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter
from .filters import productFilter, categoryFilter
from django_filters.rest_framework import DjangoFilterBackend

class productCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = productSerializer
    queryset = product.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save()
        
class productListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = productSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = productFilter
    search_fields = ['name', 'description', 'category__name']
    queryset = product.objects.all()
    
class productDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = productSerializer
    queryset = product.objects.all()
    lookup_field = 'slug'
    
    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)
    
class categoryCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = categorySerializer
    queryset = Category.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
    
class categoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = categorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = categoryFilter
    search_fields = ['name', 'description']
    queryset = Category.objects.all()
    
class categoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = categorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    def perform_update(self, serializer):
        serializer.save()