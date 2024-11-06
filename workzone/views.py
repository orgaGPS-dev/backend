from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import WorkzoneSerializer
from db.models import Workzone


def product_owner_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Überprüfen, ob der Benutzer ein `product_owner` ist
        if not request.user.is_authenticated or not request.user.product_owner:
            return Response({"error": "Unauthorized!"},
                            status=status.HTTP_403_FORBIDDEN)
        return func(request, *args, **kwargs)
    return wrapper


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@product_owner_required  # Nur `product_owner` dürfen Workzones erstellen
def create_workzone_api(request):
    serializer = WorkzoneSerializer(data=request.data)
    if serializer.is_valid():
        workzone = serializer.save()
        request.user.workzones.add(workzone)  # Zuweisung der Workzone zum Benutzer
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@product_owner_required  # Nur `product_owner` dürfen Workzones bearbeiten
def edit_workzone_api(request, workzone_id):
    try:
        workzone = Workzone.objects.get(id=workzone_id)
    except Workzone.DoesNotExist:
        return Response({"error": "Workzone not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = WorkzoneSerializer(workzone, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@product_owner_required  # Nur `product_owner` dürfen Workzones löschen
def delete_workzone_api(request, workzone_id):
    try:
        workzone = Workzone.objects.get(id=workzone_id)
    except Workzone.DoesNotExist:
        return Response({"error": "Workzone not found."}, status=status.HTTP_404_NOT_FOUND)

    workzone.delete()
    return Response({"message": "Workzone deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
