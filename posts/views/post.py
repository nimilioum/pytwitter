from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from auth_users.permissions import IsNotSuspendedOrReadOnly
from posts.models import Post
from posts.permissions import IsOwner
from posts.serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer, PostUpdateSerializer
from posts.serializers.report import ReportSerializer
from profiles.models import Profile
from utils.views import ModelViewSetWithContext, GenericViewSetWithContext


class PostVIewSet(ModelViewSetWithContext):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticated, IsNotSuspendedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['caption']
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer

        if self.action == 'update':
            return PostUpdateSerializer

        if self.action == 'retrieve':
            return PostDetailSerializer

        if self.action == 'report':
            return ReportSerializer

        if self.action in ['retweet', 'like', 'save']:
            return None

        return super().get_serializer_class()

    def retrieve(self, request, pk=None, *args, **kwargs):
        post: Post = get_object_or_404(self.queryset, pk=pk)
        comments = post.comments.all()
        comments_dict = {i.id: {'post': i, 'comments': []} for i in comments}
        for c in comments:
            reply_id = c.reply_to_id
            if reply_id is not None and reply_id != post.id:
                comments_dict[reply_id]['comments'].append(comments_dict[c.id]['post'])
        for c in comments:
            c.comments_view = comments_dict[c.id]['comments']

        post.comments_view = [i for i in comments if i.reply_to_id == post.id]

        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=False, methods=['GET', ])
    def feed(self, request, *args, **kwargs):
        user = request.user
        # followings = [i.user for i in Profile.objects.get_user_followings(user)]
        #
        # following_posts = Post.objects.filter(user__in=followings)
        # following_likes = Post.objects.filter(likes__in=followings)
        #
        # feed = (following_posts | following_likes).all().distinct()
        feed = Post.objects.all().order_by('-created_at')[:20]

        serializer = self.get_serializer(feed, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST', ])
    def retweet(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        post.retweet(request.user)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET', ], pagination_class=PageNumberPagination)
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

    @action(detail=True, methods=['POST', ])
    def report(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer: ReportSerializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['post'] = post
            serializer.validated_data['user'] = self.request.user
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUserVIewSet(GenericViewSetWithContext):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated, IsNotSuspendedOrReadOnly, IsOwner]
    pagination_class = PageNumberPagination
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'

    # def list(self, request, *args, **kwargs):
    #     posts = Post.objects.get_user_tweets(request.user)
    #     serializer = self.get_serializer(posts, many=True)
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', ], url_path='posts', url_name='posts')
    def user_posts(self, request, username=None):
        posts = Post.objects.get_user_tweets(username)
        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET', ], url_path='posts-replies', detail=True, pagination_class=PageNumberPagination)
    def user_tweets_replies(self, request, username=None, *args, **kwargs):
        posts = Post.objects.get_user_tweets_replies(username)
        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET', ], url_path='retweet-posts', detail=True, pagination_class=PageNumberPagination)
    def user_retweets(self, request, username=None, *args, **kwargs):
        posts = Post.objects.get_user_retweets(username)
        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET', ], url_path='likes', detail=True, pagination_class=PageNumberPagination)
    def user_liked_posts(self, request, username=None, *args, **kwargs):
        posts = Post.objects.get_user_likes(username)
        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get', ], url_path='bookmarks', url_name='bookmarks')
    def user_bookmarks(self, request):
        posts = Post.objects.get_user_bookmarks(request.user)
        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
