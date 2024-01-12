from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Profile
from .serializers import ProfileListSerializer, ProfileDetailSerializer, \
    ProfileUpdateSerializer, ProfileAvatarUpdateSerializer


class ProfileViewSet(GenericViewSet,
                     ListModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    lookup_field = 'user__username'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__username']

    def get_serializer_class(self):
        if self.action in ['follow']:
            return None

        if self.action == 'update':
            return ProfileUpdateSerializer

        if self.action == 'retrieve':
            return ProfileDetailSerializer

        if self.action == 'update_avatar':
            return ProfileAvatarUpdateSerializer

        return super().get_serializer_class()

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=True, methods=['POST', ])
    def follow(self, request, user__username=None):
        profile = get_object_or_404(self.queryset, user__username=user__username)
        current_profile = Profile.objects.get(user=request.user)

        current_profile.follow(profile)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST', ], url_name='avatar', url_path='avatar',
            parser_classes=[MultiPartParser])
    def update_avatar(self, request, user__username=None):
        profile = get_object_or_404(self.queryset, user__username=user__username)
        serializer = ProfileAvatarUpdateSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
