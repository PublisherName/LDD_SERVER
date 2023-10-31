from plants.views import PlantDiseaseDetectionViewSet

from django_rest_passwordreset.views import \
    ResetPasswordValidateTokenViewSet, \
    ResetPasswordConfirmViewSet, \
    ResetPasswordRequestTokenViewSet

from auths.views import \
    ServerStatusViewSet, \
    UserRegistrationViewSet, \
    UserLoginViewSet, \
    UserDetailsViewSet, \
    UserChangePasswordViewSet

from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from django.urls import path, include

from django.conf.urls import (
    handler404, 
    handler500,
  )

router = routers.DefaultRouter()

router.register(
    r'status',
    ServerStatusViewSet,
    basename='status'
)

router.register(
    r'register',
    UserRegistrationViewSet,
    basename='register'
)

router.register(
    r'login',
    UserLoginViewSet,
    basename='login'
)

router.register(
    r'forgot-password',
    ResetPasswordRequestTokenViewSet,
    basename='forgot-password'
)

router.register(
    r'validate_token',
    ResetPasswordValidateTokenViewSet,
    basename='validate-token'
)

router.register(
    r'reset-password',
    ResetPasswordConfirmViewSet,
    basename='reset-password'
)

router.register(
    r'profile',
    UserDetailsViewSet,
    basename='profile'
)

router.register(
    r'change-password',
    UserChangePasswordViewSet,
    basename='change-password'
)

router.register(
    r'plant-disease-detection',
    PlantDiseaseDetectionViewSet,
    basename='plant-disease-detection'
)


urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'api.views.error404'
handler500 = 'api.views.error500'