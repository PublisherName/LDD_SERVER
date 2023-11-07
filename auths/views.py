from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, authentication
from rest_framework.permissions import IsAuthenticated

from auths.serializers import \
    UserRegistrationSerializer , \
    UserSerializer, \
    UserLoginSerializer, \
    UserChangePasswordSerializer, \
    UserActivationSerializer


class ServerStatusViewSet(viewsets.ViewSet):
    def list(self,request):
        return Response({'status': 'Server is running'})


class UserRegistrationViewSet(viewsets.ViewSet):
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            if user:
                return Response({'status': 'User created. Please verify email to activate acccount.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivationViewSet(viewsets.ViewSet):
    serializer_class = UserActivationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.delete()
            return Response({'status': 'User activated.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(viewsets.ViewSet):
    serializer_class = UserLoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            user.token = token
            user.save()
            return Response({'token': token.key})
        else:
            return Response({'details': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


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

class UserChangePasswordViewSet(viewsets.ViewSet):
    serializer_class = UserChangePasswordSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=request.user.username, password=serializer.validated_data['old_password'])
        if user is not None:
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'Password changed'}, status=status.HTTP_200_OK)
        else:
            return Response({'details': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)