from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from .models import Profile


base_fields = ('username', 'avatar', 'bio', 'is_followed')


class ProfileBaseSerializer(ModelSerializer):
    username = serializers.SerializerMethodField(source='user__username')
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = base_fields

    def get_username(self, obj) -> str:
        if hasattr(obj, 'username'):
            return obj.username
        return obj.user.username

    def get_is_followed(self, obj):
        if user := self.context.get('user'):
            current_profile = Profile.objects.get(user=user)
            return current_profile.is_followed(current_profile)
        return False


class ProfileListSerializer(ProfileBaseSerializer):

    class Meta:
        model = Profile
        fields = base_fields


class ProfileDetailSerializer(ProfileBaseSerializer):

    class Meta:
        model = Profile
        fields = base_fields + ('followings', 'followers', )

    followings = serializers.IntegerField(source='follows_count', read_only=True)
    followers = serializers.IntegerField(source='follower_count', read_only=True)


class ProfileUpdateSerializer(ProfileBaseSerializer):
    username = serializers.CharField(source='user.username', read_only=False)

    class Meta:
        model = Profile
        fields = base_fields

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.save()
        instance = super().update(instance, validated_data)
        return instance


class ProfileAvatarUpdateSerializer(ProfileBaseSerializer):

    class Meta:
        model = Profile
        fields = base_fields
        read_only_fields = ('username', 'bio')

    def update(self, instance, validated_data):
        avatar = validated_data.pop('avatar', None)
        if avatar:
            instance.avatar = avatar
        return super().update(instance, validated_data)
