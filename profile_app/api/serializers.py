from rest_framework import serializers
from profile_app.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user','surname', 'first_name', 'middle_name', 'dob', 'address', 'bio', 'avi', 'phone_num']

    def validate_avi(self, avi):
        max_size = 2 * 1024 * 1024  # 2 MB
        if avi.size > max_size:
            raise serializers.ValidationError("File size should not exceed 2MB.")

        valid_extensions = ['jpeg', 'jpg', 'png']
        if not avi.name.split('.')[-1].lower() in valid_extensions:
            raise serializers.ValidationError("Unsupported file format. Allowed formats are: jpeg, jpg, png.")

        return avi
