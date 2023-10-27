from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, authentication
from rest_framework.permissions import IsAuthenticated

from auths.serializers import UserRegistrationSerializer , UserSerializer


class ServerStatusViewSet(viewsets.ViewSet):
    def list(self,request):
        return Response({'status': 'Server is running'})


class UserRegistrationViewSet(viewsets.ViewSet):
    serializer_class = UserRegistrationSerializer
    
    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'User created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(viewsets.ViewSet):
    def create(self, request):
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                user.token = token
                user.save()
                return Response({'token': token.key})
            else:
                return Response({'details': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'details': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        token_user = self.request.auth.user if self.request.auth else None
        if user != token_user:
            raise PermissionDenied('Token does not belong to this user')

        return User.objects.filter(pk=self.request.user.pk)