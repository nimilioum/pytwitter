from rest_framework.viewsets import ModelViewSet, GenericViewSet


class ModelViewSetWithContext(ModelViewSet):

    def get_serializer_context(self):
        if self.request.user.is_authenticated:
            return {'user': self.request.user, 'request': self.request}
        return super().get_serializer_context()


class GenericViewSetWithContext(GenericViewSet):

    def get_serializer_context(self):
        if self.request.user.is_authenticated:
            return {'user': self.request.user, 'request': self.request}
        return super().get_serializer_context()
