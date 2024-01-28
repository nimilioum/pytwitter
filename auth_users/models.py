from utils.models import Model
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Suspend(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, related_name='suspends')
    from_date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField()
