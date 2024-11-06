from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('workzone.urls')),  # API-Routen der App
    path('homepage/', include('homepage.urls')),
    path('accounts/', include('accounts.urls')), 
    path('db/', include('db.urls')), 
    path('', include('locations.urls')),
    path('', include('custom_calendar.urls')),  # URLs der custom_calendar-App einbinden
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
