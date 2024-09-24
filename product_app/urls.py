from django.urls import path
from product_app.api.views import categoryCreateView, categoryListView, categoryDetailView

urlpatterns = [
    path('create/', categoryCreateView.as_view(), name="create_category"),
    path('list/', categoryListView.as_view(), name='category_list'),
    path('detail/', categoryDetailView.as_view(), name='category_detail'),
]