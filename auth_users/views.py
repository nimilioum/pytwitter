from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from .serializers import RegisterSerializer


class UserViewSet(GenericViewSet,
                  CreateModelMixin):
    serializer_class = RegisterSerializer
