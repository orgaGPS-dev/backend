from rest_framework.response import Response
from rest_framework.views import APIView

class WelcomeText(APIView):
    def get(self, request):
        welcome_text = "OrgaGPS is the smart solution for efficient and reliable scheduling, designed to streamline time management for both businesses and individuals. Leveraging precise GPS technology, this app allows employees to confirm their presence at designated locations with a single tap, enabling companies to track attendance accurately and effortlessly. With a focus on both technical precision and ease of use, OrgaGPS brings a new level of efficiency to scheduling—whether for corporate operations or personal use. Discover how OrgaGPS can transform the way you plan, manage, and optimize time."
        return Response({"welcome_text": welcome_text})

class GPSTrackingText(APIView):
    def get(self, request):
        data = {
            "title": "GPS Tracking",
            "description": "Real-time tracking for better oversight."
        }
        return Response(data)

class ShiftSchedulingText(APIView):
    def get(self, request):
        data = {
            "title": "Shift Scheduling",
            "description": "Easy shift planning with just a few clicks."
        }
        return Response(data)

class TaskManagementText(APIView):
    def get(self, request):
        data = {
            "title": "Task Management",
            "description": "Clear tasks, better results."
        }
        return Response(data)

class ReportsAnalyticsText(APIView):
    def get(self, request):
        data = {
            "title": "Reports and Analytics",
            "description": "Leverage data for smarter decisions."
        }
        return Response(data)

class TheVisionText(APIView):
    def get(self, request):
        vision_text = "At OrgaGPS, we aim to make organizing time and tasks simpler and more intuitive, whether for businesses or personal use. A flexible scheduling tool designed for companies and individuals alike, to stay effortlessly on top of their plans with a quick GPS check-in. With just a tap on their phones, team members can confirm their presence at designated GPS locations—making it easy for employers to track attendance and timeliness in a straightforward, efficient, and enjoyable way. By supporting companies in maintaining smooth operations and helping individuals manage their commitments with ease, OrgaGPS is here to bring simplicity and reliability to everyone’s day."
        return Response({"the_vision_text": vision_text})
