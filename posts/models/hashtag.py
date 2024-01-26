from django.db import models
from utils.models import Model


class Hashtag(Model):
    name = models.CharField(max_length=100)
