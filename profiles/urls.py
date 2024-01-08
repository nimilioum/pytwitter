from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

router = DefaultRouter()
router.register('user', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
]
