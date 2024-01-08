from django.db import models, IntegrityError
from utils import Model, DomainException
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/avatars', null=True, blank=True)

    def follow(self, user: User):
        try:
            self.follows.add(user.profile)
        except IntegrityError:
            raise DomainException('User is already followed')

    def unfollow(self, user: User):
        self.follows.remove(user.profile)

    def is_followed(self, user: User):
        return Profile.objects.filter(follows=user.profile, id=self.id).exists()
