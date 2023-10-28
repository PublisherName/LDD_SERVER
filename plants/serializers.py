import os
from rest_framework import serializers
import os
import uuid
from roboflow import Roboflow
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


try:
    Roboflow_Connection_Error = False
    project = Roboflow(api_key=os.environ['ROBO_FLOW_API_KEY']).workspace(
    ).project("leaf-disease-detection-mpdfi")
    model = project.version(3).model
except:
    Roboflow_Connection_Error = True


class PlantDiseaseDetectionSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def create(self, validated_data):

        image_file = validated_data['image']

        if not Roboflow_Connection_Error:

            image_name = f"{uuid.uuid4().hex}.{image_file.name.split('.')[-1]}"
            upload_image_path = os.path.join(
                settings.MEDIA_ROOT, 'plants_uploaded', image_name)
            detected_image_path = os.path.join(
                settings.MEDIA_ROOT, 'plants_detected', f"{uuid.uuid4().hex}.jpg")
            with open(upload_image_path, 'wb') as f:
                f.write(image_file.read())

            try:
                result = model.predict(
                    upload_image_path, confidence=40, overlap=30).json()
                for predictions in result['predictions']:
                    model.predict(predictions['image_path'], confidence=40, overlap=30).save(
                        detected_image_path)
                    os.remove(predictions['image_path'])
                    predictions.pop('image_path')
                    predictions['detection_image'] = detected_image_path
            except Exception as e:
                os.remove(upload_image_path)
                raise serializers.ValidationError({'details': 'Unable to predict sample.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return result
        else:
           raise serializers.ValidationError({'details': 'Unable to connect to ML model.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
