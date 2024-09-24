from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProfileCreateView, ProfileListView, ProfileDetailView

urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name="create_profile"),
    path('lists/', ProfileListView.as_view(), name="profile_lists"),
    path('details/<slug:user__username>/', ProfileDetailView.as_view(), name="profile_details")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)