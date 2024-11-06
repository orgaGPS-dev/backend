from django.urls import path
from . import views

urlpatterns = [
    path('api/workzone/create/', views.create_workzone_api, name='create_workzone_api'),
    path('api/workzone/edit/<int:workzone_id>/', views.edit_workzone_api, name='edit_workzone_api'),
    path('api/workzone/delete/<int:workzone_id>/', views.delete_workzone_api, name='delete_workzone_api'),
]
