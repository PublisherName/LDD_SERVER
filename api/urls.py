from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from auths.views import ServerStatusViewSet, UserRegistrationViewSet, UserLoginViewSet, UserDetailsViewSet, UserChangePasswordViewSet

from plants.views import PlantDiseaseDetectionViewSet

router = routers.DefaultRouter()
router.register(r'status', ServerStatusViewSet, basename='status')
router.register(r'register', UserRegistrationViewSet, basename='register')
router.register(r'login', UserLoginViewSet, basename='login')
router.register(r'profile', UserDetailsViewSet, basename='profile')
router.register(r'change-password', UserChangePasswordViewSet, basename='change-password')
router.register(r'plant-disease-detection', PlantDiseaseDetectionViewSet, basename='plant-disease-detection')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
