from django.db import transaction
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from profiles.serializers import ProfileBaseSerializer
from posts.models import Post, Upload

post_fields = ('id', 'user', 'caption', 'files', 'likes', 'retweets', 'reply_to',
               'mentions', 'hashtags', 'created_at')


class UploadListSerializer(ModelSerializer):
    class Meta:
        model = Upload
        fields = (
            'file', 'id'
        )


class CommentListSerializer(ModelSerializer):
    user = ProfileBaseSerializer()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = post_fields + ('comments',)

    @staticmethod
    def get_comments(obj):
        return CommentListSerializer(obj.comments_view, many=True).data


class PostBaseSerializer(ModelSerializer):
    user = ProfileBaseSerializer()
    likes = serializers.IntegerField(source='likes_count', read_only=True)
    retweets = serializers.IntegerField(source='retweets_count', read_only=True)
    files = UploadListSerializer(many=True, read_only=True)
    hashtags = serializers.HyperlinkedRelatedField(view_name='hashtags-posts', read_only=True,
                                                   many=True, lookup_field='name')
    mentions = serializers.HyperlinkedRelatedField(view_name='profiles-detail', many=True, read_only=True,
                                                      lookup_field='username')
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = post_fields

    def get_replies_count(self, obj):
        return obj.replies_count


class PostCreateSerializer(PostBaseSerializer):
    files = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False,
                                    required=False), write_only=True, required=False,
    )

    class Meta:
        model = Post
        fields = ('id', 'caption', 'reply_to', 'files')

    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get('user')

        if 'files' in validated_data:
            files = validated_data.pop('files')
            post = Post.objects.create(user=user, **validated_data)
            files_create = []
            for file in files:
                files_create.append(Upload(post=post, file=file))
            Upload.objects.bulk_create(files_create)
        else:
            post = Post.objects.create(user=user, **validated_data)
        return post


class PostUpdateSerializer(PostBaseSerializer):
    files_add = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False,
                                    required=False), write_only=True, required=False,
    )

    files_remove = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Post
        fields = ('id', 'caption', 'files_add', 'files_remove')

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
        fields = post_fields + ('replies_count',)


class PostDetailSerializer(PostBaseSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = post_fields + ('comments', 'replies_count',)

    def get_comments(self, obj):
        return CommentListSerializer(obj.comments_view, many=True).data
