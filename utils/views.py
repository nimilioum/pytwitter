from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin


class UserSerializerMixin:

    def get_serializer_context(self):
        if self.request.user.is_authenticated:
            return {'user': self.request.user}
        return super().get_serializer_context()

