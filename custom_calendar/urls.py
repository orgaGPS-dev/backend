from django.urls import path
from .views import user_schedule_list, create_schedule, edit_schedule, delete_schedule, mark_attendance

urlpatterns = [
    path('api/calendar/', user_schedule_list, name='user_schedule_list'),  # Alle Termine des Benutzers abrufen
    path('api/calendar/create/', create_schedule, name='create_schedule'),  # Neues Event erstellen
    path('api/calendar/edit/<int:schedule_id>/', edit_schedule, name='edit_schedule'),  # Event bearbeiten
    path('api/calendar/delete/<int:schedule_id>/', delete_schedule, name='delete_schedule'),  # Event löschen
    path('api/calendar/attendance/<int:schedule_id>/', mark_attendance, name='mark_attendance'),

]
