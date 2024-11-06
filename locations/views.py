# locations/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import LocationSerializer
from db.models import Location

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_location(request):
    # Überprüfen, ob der Benutzer die Berechtigung zum Hinzufügen einer Location hat
    if not hasattr(request.user, 'permissions') or not request.user.permissions.can_add_location:
        return Response({"error": "Unauthorized. You do not have permission to add locations."},
                        status=status.HTTP_403_FORBIDDEN)
    
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_locations(request):
    # Jeder authentifizierte Benutzer kann die Liste der Locations abrufen
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_location(request, location_id):
    # Überprüfen, ob der Benutzer die Berechtigung zum Bearbeiten einer Location hat
    if not hasattr(request.user, 'permissions') or not request.user.permissions.can_edit_location:
        return Response({"error": "Unauthorized. You do not have permission to edit locations."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({"error": "Location not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = LocationSerializer(location, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_location(request, location_id):
    # Überprüfen, ob der Benutzer die Berechtigung zum Löschen einer Location hat
    if not hasattr(request.user, 'permissions') or not request.user.permissions.can_delete_location:
        return Response({"error": "Unauthorized. You do not have permission to delete locations."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({"error": "Location not found."}, status=status.HTTP_404_NOT_FOUND)

    location.delete()
    return Response({"message": "Location deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
