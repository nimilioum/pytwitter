from django.db import models, IntegrityError
from utils import Model, DomainException
from django.contrib.auth import get_user_model
from .managers import ProfileManager

User = get_user_model()


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/avatars', null=True, blank=True)
    objects = ProfileManager()

    def follow(self, profile: "Profile"):
        follows = self.follows.all()
        if profile not in follows:
            self._follow(profile)
        else:
            self._unfollow(profile)

    def _follow(self, profile: "Profile"):
        try:
            self.follows.add(profile)
        except IntegrityError:
            raise DomainException('User is already followed')

    def _unfollow(self, profile: "Profile"):
        self.follows.remove(profile)

    def is_followed(self, profile: "Profile"):
        return Profile.objects.filter(follows=profile, id=self.id).exists()
