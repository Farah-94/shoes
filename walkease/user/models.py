from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)  # renamed field and increased max_length if needed
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"