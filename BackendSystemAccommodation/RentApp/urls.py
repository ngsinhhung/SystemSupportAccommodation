from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='Users')
router.register('post', PostViewSet, basename='Post')
router.register('comment', CommentPostViewSet, basename='CommentPost')
router.register('accommodation', AccommodationViewSet, basename='Accommodation')

urlpatterns = [
    path('', include(router.urls))
]