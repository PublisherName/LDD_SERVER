import os
import uuid
import base64
import requests
from rest_framework import serializers

from django.conf import settings

class PlantDiseaseDetectionSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    def create(self, validated_data):

        image_file = validated_data['image']
        image_ext = image_file.name.split('.')[-1]
        image_name = f"{uuid.uuid4().hex}.{image_ext}"
        
        upload_image_path = os.path.join(
            settings.MEDIA_ROOT, 'plants_uploaded', image_name)
        
        upload_image_url = os.path.join(
            settings.MEDIA_URL, 'plants_uploaded', image_name)

        with open(upload_image_path, 'wb') as f:
            f.write(image_file.read())

        image_file = open(upload_image_path, 'rb')
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        try:
            url = os.environ['ROBO_FLOW_API_URL']
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=encoded_image)
            if response.status_code == 200:
                result = response.json()
                for predictions in result['predictions']:
                    predictions['image'] = upload_image_url
                return result
            else:
                os.remove(upload_image_path)
                return {'details': 'Please try again later.'}
        except:
            os.remove(upload_image_path)
            return {'details': 'Please try again later.'}
