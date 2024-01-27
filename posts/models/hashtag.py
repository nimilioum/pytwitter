from django.db import models
from utils.models import Model


class Hashtag(Model):
    name = models.CharField(max_length=100, unique=True)

    def get_posts(self):
        return self.posts.all()

    def __str__(self):
        return self.name
