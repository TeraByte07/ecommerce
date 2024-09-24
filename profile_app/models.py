from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    surname = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    bio = models.TextField(max_length=255, blank=True, null=True)
    avi = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone_num = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.user.username}\'s profile details'
