from .serializers import UserProfileSerializer
from profile_app.models import UserProfile
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAccountOwner
from rest_framework.exceptions import ValidationError

class ProfileCreateView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    
    def perform_create(self, serializer):
        user=self.request.user
        if UserProfile.objects.filter(user=user).exists():
            raise ValidationError({"detail": "You have already created a profile."})
        serializer.save(user=user)
        
class ProfileListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all()
        
class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAccountOwner]
    queryset = UserProfile.objects.all()
    lookup_field = "user__username"
    
    def perform_update(self, serializer):
        serializer.save()
