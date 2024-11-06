from datetime import datetime, timedelta
import calendar
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ScheduleSerializer
from db.models import Schedule
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from db.models import Schedule
import math


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_schedule_list(request):
    schedules = Schedule.objects.filter(user=request.user)
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_schedule(request):
    if not hasattr(request.user, 'permissions') or not request.user.permissions.can_add_schedule:
        return Response({"error": "Unauthorized. You do not have permission to add schedules."},
                        status=status.HTTP_403_FORBIDDEN)
    
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        schedule = serializer.save(user=request.user)  # Originalereignis speichern

        # Überprüfen, ob das Ereignis wiederkehrend ist und Wochentage definiert sind
        if schedule.is_recurring and schedule.recurrence_days:
            generate_recurring_events_for_month(request.user, schedule)  # Wiederholungen erstellen

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Helper-Funktion zur Generierung wiederkehrender Ereignisse für den Monat
def generate_recurring_events_for_month(user, schedule):
    today = datetime.today()
    _, last_day = calendar.monthrange(today.year, today.month)
    current_date = today.replace(day=1)
    recurring_events = []

    while current_date.day <= last_day:
        # Prüfen, ob der aktuelle Tag in den gewählten Wochentagen enthalten ist
        if current_date.strftime("%A") in schedule.recurrence_days:
            new_event = Schedule(
                user=user,
                event_name=schedule.event_name,
                start_time=current_date.replace(hour=schedule.start_time.hour, minute=schedule.start_time.minute),
                end_time=current_date.replace(hour=schedule.end_time.hour, minute=schedule.end_time.minute),
                description=schedule.description,
                is_recurring=True,
                recurrence_pattern=schedule.recurrence_pattern,
                recurrence_days=schedule.recurrence_days,
                category=schedule.category
            )
            recurring_events.append(new_event)
        
        current_date += timedelta(days=1)  # Zum nächsten Tag wechseln
    
    # Alle Termine auf einmal speichern
    Schedule.objects.bulk_create(recurring_events)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_schedule(request, schedule_id):
    if not hasattr(request.user, 'permissions') or not request.user.permissions.can_edit_schedule:
        return Response({"error": "Unauthorized. You do not have permission to edit schedules."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        schedule = Schedule.objects.get(id=schedule_id, user=request.user)
    except Schedule.DoesNotExist:
        return Response({"error": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

    # Bearbeitung für alle zugehörigen Ereignisse, wenn `is_recurring=True` (optional)
    apply_to_all = request.data.get('apply_to_all', False)
    
    if apply_to_all and schedule.is_recurring:
        related_events = Schedule.objects.filter(
            user=request.user,
            event_name=schedule.event_name,
            recurrence_pattern=schedule.recurrence_pattern,
            recurrence_days=schedule.recurrence_days,
            start_time__month=schedule.start_time.month  # Falls monatliche Wiederholung gewünscht
        )
        for event in related_events:
            serializer = ScheduleSerializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
    else:
        serializer = ScheduleSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_schedule(request, schedule_id):
    if not hasattr(request.user, 'permissions') or not request.user.permissions.can_delete_schedule:
        return Response({"error": "Unauthorized. You do not have permission to delete schedules."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        schedule = Schedule.objects.get(id=schedule_id, user=request.user)
    except Schedule.DoesNotExist:
        return Response({"error": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

    # Löschen aller zugehörigen Ereignisse, falls gewünscht
    delete_all = request.query_params.get('delete_all', 'false').lower() == 'true'

    if delete_all and schedule.is_recurring:
        Schedule.objects.filter(
            user=request.user,
            event_name=schedule.event_name,
            recurrence_pattern=schedule.recurrence_pattern,
            recurrence_days=schedule.recurrence_days,
            start_time__month=schedule.start_time.month
        ).delete()
        return Response({"message": "All recurring events deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    schedule.delete()
    return Response({"message": "Schedule deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



def calculate_distance(lat1, lon1, lat2, lon2):
    """Berechnet die Entfernung zwischen zwei GPS-Koordinaten in Metern."""
    R = 6371.0  # Erdradius in Kilometern
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000  # Rückgabe der Distanz in Metern

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendance(request, schedule_id):
    """Markiert die Anwesenheit eines Benutzers basierend auf seinem Standort und der Nähe zur Location."""
    try:
        schedule = Schedule.objects.get(id=schedule_id, user=request.user)
    except Schedule.DoesNotExist:
        return Response({"error": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

    # Ermittlung der zugehörigen Workzone des Benutzers
    if not request.user.workzones.exists():
        return Response({"error": "User is not associated with any workzone."}, status=status.HTTP_400_BAD_REQUEST)

    workzone = request.user.workzones.first()
    distance_unit = workzone.distance_unit  # 'm' für Meter oder 'ft' für Feet

    # GPS-Koordinaten des Benutzers auslesen
    try:
        user_lat = float(request.data.get('latitude'))
        user_lon = float(request.data.get('longitude'))
    except (TypeError, ValueError):
        return Response({"error": "Invalid GPS coordinates."}, status=status.HTTP_400_BAD_REQUEST)

    # Überprüfen, ob Location-Daten in Schedule existieren
    if not schedule.location or not schedule.location.location_gps_data:
        return Response({"error": "Location data is missing for this schedule."}, status=status.HTTP_400_BAD_REQUEST)

    # GPS-Daten und Radius der Location extrahieren
    loc_lat, loc_lon = map(float, schedule.location.location_gps_data.split(','))
    location_radius = float(schedule.location.location_radius)

    # Radius abhängig von der Einheit (Meter oder Feet) konvertieren
    if distance_unit == 'ft':
        location_radius *= 3.28084  # Umrechnen von Metern in Fuß

    # Entfernung berechnen und mit Radius vergleichen
    distance = calculate_distance(loc_lat, loc_lon, user_lat, user_lon)
    if distance > location_radius:
        return Response({"error": "Outside the allowed radius for attendance."}, status=status.HTTP_403_FORBIDDEN)

    # Anwesenheit bestätigen und Pünktlichkeit speichern
    current_time = datetime.now()
    schedule.login_time = current_time
    schedule.punctual = current_time <= schedule.start_time_login
    schedule.save()

    return Response({"status": "Attendance marked successfully.", "punctual": schedule.punctual}, status=status.HTTP_200_OK)
