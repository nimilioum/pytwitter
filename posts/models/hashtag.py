from django.db import models
from posts.models import Post
from utils.models import Model


class Hashtag(Model):
    name = models.CharField(max_length=100)


class PostHashtag(Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
