from rest_framework import serializers

from posts.models import Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    posts = serializers.IntegerField(source='post_count', read_only=True)

    class Meta:
        model = Hashtag
        fields = ('name', 'posts')
