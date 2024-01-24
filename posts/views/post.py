from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.viewsets import ModelViewSet

from profiles.serializers import ProfileListSerializer
from profiles.models import Profile

from posts.serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer, PostUpdateSerializer

from posts.models import Post
from utils import UserSerializerMixin


class PostVIewSet(ModelViewSet, UserSerializerMixin):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer

        if self.action == 'update':
            return PostUpdateSerializer

        if self.action == 'retrieve':
            return PostDetailSerializer

        if self.action == 'retweets':
            return ProfileListSerializer

        if self.action in ['retweet', 'like', 'save']:
            return None

        return super().get_serializer_class()

    @action(detail=True, methods=['POST', ])
    def retweet(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        post.retweet(request.user)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET', ])
    def retweets(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        retweets = post.retweets.all()
        users = Profile.objects.filter(user__in=retweets)
        serializer = PostListSerializer(users, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['POST', ])
    def like(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        post.like(request.user)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST', ])
    def save(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        post.save_post(request.user)

        return Response(status=status.HTTP_201_CREATED)


