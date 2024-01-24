from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='Users')
router.register('hostpost', HostPostViewSet, basename='HostPost')

urlpatterns = [
    path('', include(router.urls))
]