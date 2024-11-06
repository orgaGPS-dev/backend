# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Workzone(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    DISTANCE_UNIT_CHOICES = [
        ('m', 'Meter'),
        ('ft', 'Feet'),
    ]
    distance_unit = models.CharField(
        max_length=2,
        choices=DISTANCE_UNIT_CHOICES,
        default='m',  # Standardmäßig in Meter
        help_text="Preferred distance unit for all users in this workzone"
    )

class CustomUser(AbstractUser):
    product_owner = models.BooleanField(default=False)
    first_login = models.BooleanField(default=True)
    workzones = models.ManyToManyField(Workzone)
    image = models.ImageField(upload_to='pics/', null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    phone1 = models.CharField(max_length=200, blank=True, null=True)
    phone2 = models.CharField(max_length=200, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    

class Location(models.Model):
    location_name = models.CharField(max_length=200)
    location_first_name = models.CharField(max_length=200)
    location_last_name = models.CharField(max_length=200)
    location_email = models.EmailField(max_length=200)
    location_phone1 = models.CharField(max_length=200, blank=True, null=True)
    location_phone2 = models.CharField(max_length=200, blank=True, null=True)
    location_address1 = models.CharField(max_length=200, blank=True, null=True)
    location_address2 = models.CharField(max_length=200, blank=True, null=True)
    location_zip_code = models.CharField(max_length=200, blank=True, null=True)
    location_city = models.CharField(max_length=200, blank=True, null=True)
    location_country = models.CharField(max_length=200, blank=True, null=True)
    location_gps_data = models.CharField(max_length=100, help_text="Latitude and Longitude in 'lat,lon' format")
    location_radius = models.DecimalField(max_digits=4, decimal_places=1, default=1.0, help_text="Radius in meters")
    location_notes = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.object_name} ({self.gps_data})"

class Schedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='schedules')
    event_name = models.CharField(max_length=200)
    start_time = models.DateTimeField(blank=True, null=True)
    start_time_login = models.DateTimeField(blank=True, null=True)
    end_time_login = models.DateTimeField(blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    start_time_logout = models.DateTimeField(blank=True, null=True)
    end_time_logout = models.DateTimeField(blank=True, null=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="schedules")  # Verbindung zur Location
    status = models.CharField(max_length=100, default='white')
    punctual = models.BooleanField(default=False)

class Permissions(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='permissions')
    can_add_customuser = models.BooleanField(default=False)
    can_edit_customuser = models.BooleanField(default=False)
    can_delete_customuser = models.BooleanField(default=False)
    can_add_locations = models.BooleanField(default=False)
    can_edit_locations = models.BooleanField(default=False)
    can_delete_locations = models.BooleanField(default=False)
    can_add_schedule = models.BooleanField(default=False)
    can_edit_schedule = models.BooleanField(default=False)
    can_delete_schedule = models.BooleanField(default=False)

class UserGroup(models.Model):
    workzone = models.ForeignKey(Workzone, on_delete=models.CASCADE, related_name='user_groups')
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_group")

    class Meta:
        unique_together = ('workzone', 'name')
