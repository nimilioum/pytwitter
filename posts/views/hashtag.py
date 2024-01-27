from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from posts.models import Hashtag
from posts.serializers import PostListSerializer
from posts.serializers.hashtag import HashtagSerializer
from utils.views import GenericViewSetWithContext


class HashtagViewSet(GenericViewSetWithContext):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    lookup_field = 'name'

    def get_serializer_class(self):
        if self.action == 'posts':
            return PostListSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        hashtags = self.queryset.all()
        serializer = self.get_serializer(hashtags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET', ], url_path='posts', name='posts', detail=True)
    def posts(self, request, name=None, *args, **kwargs):
        hashtag = get_object_or_404(self.queryset, name=name)
        posts = hashtag.get_posts()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
