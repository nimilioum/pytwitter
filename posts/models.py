from django.db import models
from utils.models import Model
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    caption = models.TextField(max_length=1000)
    retweets = models.ManyToManyField(User, related_name='retweets')
    likes = models.ManyToManyField(User, related_name='liked_posts')
    saves = models.ManyToManyField(User, related_name='saved_posts')


class Comment(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(max_length=1000)
