# serializers.py

from rest_framework import serializers
from .models import CustomUser, Workzone, Location, Schedule, Permissions, UserGroup

#Workzone
class WorkzoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workzone
        fields = '__all__'

#Custom User
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserFirstNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name']  # Only include the first_name field

#Location
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

#Schedule
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

#Permissions
class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'

#User Groups
class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'
