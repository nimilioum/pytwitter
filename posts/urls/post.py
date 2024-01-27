from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import PostVIewSet, PostUserVIewSet

router = DefaultRouter()
router.register('', PostVIewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]
