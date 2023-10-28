from django.urls import path, include
from rest_framework import routers

from auths.views import ServerStatusViewSet, UserRegistrationViewSet, UserLoginViewSet, UserDetailsViewSet, UserChangePasswordViewSet


router = routers.DefaultRouter()
router.register(r'status', ServerStatusViewSet, basename='status')
router.register(r'register', UserRegistrationViewSet, basename='register')
router.register(r'login', UserLoginViewSet, basename='login')
router.register(r'profile', UserDetailsViewSet, basename='profile')
router.register(r'change-password', UserChangePasswordViewSet, basename='change-password')


urlpatterns = [
    path('', include(router.urls)),
]
