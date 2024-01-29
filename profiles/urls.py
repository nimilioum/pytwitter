from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ProfileUpdateViewSet

router = DefaultRouter()
router.register('', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
    path('update', ProfileUpdateViewSet.as_view(
        {'put': 'update'}
    ), name='profile-update'),
    path('avatar', ProfileUpdateViewSet.as_view(
        {'post': 'update_avatar'}
    ))
]
