from django.urls import path,include
from django.http import HttpResponse

def server_status(request):
    return HttpResponse('Server is running', status=200)


urlpatterns = [
     path('auth/', include('rest_registration.api.urls')),
     path('status/', server_status),
]
