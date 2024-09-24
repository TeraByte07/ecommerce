import django_filters
from product_app.models import product

class productFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name = "price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    search = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    
    class Meta:
        model = product
        fields = ['category', 'min_price', 'max_price', 'search']
        
class categoryFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    search = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    
    class Meta:
        model = product
        fields = ['category', 'search']