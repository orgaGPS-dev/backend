from django.urls import path
from .views import (
    WelcomeText,
    GPSTrackingText,
    ShiftSchedulingText,
    TaskManagementText,
    ReportsAnalyticsText,
    TheVisionText
)

urlpatterns = [
    path('api/homepage_welcome-text/', WelcomeText.as_view(), name='homepage_welcome_text'),
    path('api/homepage_features-text/gps-tracking/', GPSTrackingText.as_view(), name='homepage_features_text_gps_tracking'),
    path('api/homepage_features-text/shift-scheduling/', ShiftSchedulingText.as_view(), name='homepage_features_text_shift_scheduling'),
    path('api/homepage_features-text/task-management/', TaskManagementText.as_view(), name='homepage_features_text_task_management'),
    path('api/homepage_features-text/reports-analytics/', ReportsAnalyticsText.as_view(), name='homepage_features_text_reports_analytics'),
    path('api/homepage_the-vision-text/', TheVisionText.as_view(), name='homepage_the_vision_text'),
]
