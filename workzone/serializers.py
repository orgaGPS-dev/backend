from rest_framework import serializers
from db.models import Workzone

class WorkzoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workzone
        fields = ['id', 'name', 'address1', 'address2', 'zip_code', 'city', 'country']
