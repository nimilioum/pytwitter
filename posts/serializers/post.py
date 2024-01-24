from django.db import transaction
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from profiles.serializers import ProfileBaseSerializer
from posts.models import Post, Upload

post_fields = ('user', 'caption', 'files', 'likes', 'retweets', 'reply_to')


class UploadListSerializer(ModelSerializer):
    class Meta:
        model = Upload
        fields = (
            'file', 'id'
        )


class CommentListSerializer(ModelSerializer):
    user = ProfileBaseSerializer()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def get_replies(obj):
        return CommentListSerializer(obj).data


class PostBaseSerializer(ModelSerializer):
    user = ProfileBaseSerializer()
    likes = serializers.IntegerField(source='likes_count', read_only=True)
    retweets = serializers.IntegerField(source='retweets_count', read_only=True)
    files = UploadListSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(PostBaseSerializer):
    files = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False,
                                    required=False)
    )

    class Meta:
        model = Post
        fields = ('caption', 'reply_to', 'files')

    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get('user')
        post = Post.objects.create(user=user, **validated_data)

        if 'files' in validated_data:
            files = validated_data.pop('files')
            for file in files:
                Upload.objects.create(post=post, file=file)
        return post


class PostUpdateSerializer(PostBaseSerializer):
    files_add = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False,
                                    required=False)
    )

    files_remove = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Post
        fields = ('caption', 'files_add', 'files_remove')

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.caption = validated_data.pop('caption', instance.caption)
        instance.save()

        if 'files_add' in validated_data:
            files = validated_data.pop('files_add')
            for file in files:
                Upload.objects.create(post=instance, file=file)

        if 'files_remove' in validated_data:
            files = validated_data.pop('files_remove')
            Upload.objects.filter(id__in=files).delete()

        return instance


class PostListSerializer(PostBaseSerializer):
    class Meta:
        model = Post
        fields = post_fields


class PostDetailSerializer(PostBaseSerializer):
    comments = CommentListSerializer()

    class Meta:
        model = Post
        fields = post_fields + ('comments',)
