from django.db import models

from posts.models import Post
from utils.models import Model
from django.contrib.auth import get_user_model

User = get_user_model()


class Report(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    description = models.TextField()
