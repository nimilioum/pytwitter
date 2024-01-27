from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import HashtagViewSet

router = DefaultRouter()
router.register('', HashtagViewSet, basename='hashtags')

urlpatterns = [
    path('', include(router.urls)),
]
