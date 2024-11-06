from django.urls import path
from . import views

urlpatterns = [
    path('api/locations/', views.list_locations, name='list_locations'),  # Alle Locations auflisten
    path('api/locations/create/', views.create_location, name='create_location'),  # Neue Location erstellen
    path('api/locations/edit/<int:location_id>/', views.edit_location, name='edit_location'),  # Location bearbeiten
    path('api/locations/delete/<int:location_id>/', views.delete_location, name='delete_location'),  # Location löschen
]
