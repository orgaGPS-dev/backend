# urls.py

from django.urls import path
from .views import (
    WorkzoneListCreateView,
    WorkzoneDetailView,
    CustomUserListCreateView,
    CustomUserDetailView,
    CustomUserFirstNameView,
    LocationListCreateView,
    LocationDetailView,
    ScheduleListCreateView,
    ScheduleDetailView,
    PermissionsListCreateView,
    PermissionsDetailView,
    UserGroupListCreateView,
    UserGroupDetailView,
)

urlpatterns = [
    # Workzone URLs
    path('api/workzones/', WorkzoneListCreateView.as_view(), name='workzone-list-create'),
    path('api/workzones/<int:pk>/', WorkzoneDetailView.as_view(), name='workzone-detail'),

    # CustomUser URLs
    path('api/users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('api/users/first-name/', CustomUserFirstNameView.as_view(), name='user-first-name-list'),  # New endpoint

    # Location URLs
    path('api/locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('api/locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),

    # Schedule URLs
    path('api/schedules/', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('api/schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),

    # Permissions URLs
    path('api/permissions/', PermissionsListCreateView.as_view(), name='permissions-list-create'),
    path('api/permissions/<int:pk>/', PermissionsDetailView.as_view(), name='permissions-detail'),

    # UserGroup URLs
    path('api/usergroups/', UserGroupListCreateView.as_view(), name='usergroup-list-create'),
    path('api/usergroups/<int:pk>/', UserGroupDetailView.as_view(), name='usergroup-detail'),
]
