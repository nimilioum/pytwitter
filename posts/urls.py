from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostVIewSet

router = DefaultRouter()
router.register('', PostVIewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
]
