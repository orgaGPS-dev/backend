# views.py

from rest_framework import generics
from .models import CustomUser, Workzone, Location, Schedule, Permissions, UserGroup
from .serializers import (
    CustomUserFirstNameSerializer,
    CustomUserSerializer,
    WorkzoneSerializer,
    LocationSerializer,
    ScheduleSerializer,
    PermissionsSerializer,
    UserGroupSerializer,
)

# Workzone Views
class WorkzoneListCreateView(generics.ListCreateAPIView):
    queryset = Workzone.objects.all()
    serializer_class = WorkzoneSerializer

class WorkzoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workzone.objects.all()
    serializer_class = WorkzoneSerializer

# CustomUser Views
class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserFirstNameView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserFirstNameSerializer
# Location Views
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# Schedule Views
class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

# Permissions Views
class PermissionsListCreateView(generics.ListCreateAPIView):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer

class PermissionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer

# UserGroup Views
class UserGroupListCreateView(generics.ListCreateAPIView):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer

class UserGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
