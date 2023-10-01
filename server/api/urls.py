from django.urls import path,include

urlpatterns = [
     path('auth/', include('rest_registration.api.urls')),
]
