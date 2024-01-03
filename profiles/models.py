from django.db import models
from utils.models import Model
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
