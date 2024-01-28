from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import PostVIewSet, PostUserVIewSet

router = DefaultRouter()
router.register('', PostUserVIewSet, basename='user_posts')

urlpatterns = [
    path('', include(router.urls)),
]
