from rest_framework import viewsets, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import PlantDiseaseDetectionSerializer

class PlantDiseaseDetectionViewSet(viewsets.ViewSet):
    serializer_class = PlantDiseaseDetectionSerializer
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = PlantDiseaseDetectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result)
    