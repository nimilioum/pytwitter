from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import PostVIewSet, PostUserVIewSet
from profiles.views import ProfileViewSet

router = DefaultRouter()
router.register('', ProfileViewSet, basename='profiles')
router.register('posts', PostUserVIewSet, basename='user_posts')

urlpatterns = [
    path('', include(router.urls)),
]
