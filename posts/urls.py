from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostVIewSet, PostUserVIewSet

router = DefaultRouter()
router.register('', PostVIewSet, basename='posts')
router.register('user', PostUserVIewSet, basename='user_posts')

urlpatterns = [
    path('', include(router.urls)),
]
