from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Directory(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.URLField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
