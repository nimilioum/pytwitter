from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from auth_users.permissions import IsNotSuspendedOrReadOnly
from utils import GenericViewSetWithContext
from .models import Profile
from .serializers import ProfileListSerializer, ProfileDetailSerializer, \
    ProfileUpdateSerializer, ProfileAvatarUpdateSerializer


class ProfileViewSet(GenericViewSetWithContext, ListModelMixin, RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__username']
    permission_classes = [IsAuthenticated, IsNotSuspendedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['follow']:
            return None

        if self.action == 'retrieve':
            return ProfileDetailSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=['POST', ])
    def follow(self, request, username=None):
        profile = get_object_or_404(self.queryset, user__username=username)
        current_profile = Profile.objects.get(user=request.user)

        current_profile.follow(profile)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET', ])
    def followings(self, request):
        followings = Profile.objects.get_user_followings(self.request.user)
        serializer = self.get_serializer(followings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET', ])
    def followers(self, request):
        followings = Profile.objects.get_user_followers(self.request.user)
        serializer = self.get_serializer(followings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class ProfileUpdateViewSet(GenericViewSetWithContext, UpdateModelMixin):

    serializer_class = ProfileUpdateSerializer
    queryset = Profile.objects.all()

    def get_serializer_class(self):

        if self.action == 'update':
            return ProfileUpdateSerializer

        if self.action == 'update_avatar':
            return ProfileAvatarUpdateSerializer

        return super().get_serializer_class()

    def get_object(self):
        return self.request.user.profile

    @action(detail=False, methods=['POST', ], url_name='avatar', url_path='avatar',
            parser_classes=[MultiPartParser])
    def update_avatar(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileAvatarUpdateSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
