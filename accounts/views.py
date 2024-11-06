# accounts/views.py

from django.contrib.auth import get_user_model, login
from rest_framework import generics, status, views
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from orgagps.tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from db.models import CustomUser, Permissions
from .serializers import RegistrationSerializer, UserInfosSerializer, ActivateAccountSerializer
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import PasswordResetRequestSerializer, PasswordResetSerializer
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import CanEditUser, CanDeleteUser


User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

# Registrierung
class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        
        # Account Aktivierung per Klartext-E-Mail senden
        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = f"http://{current_site.domain}/activate?uid={uid}&token={token}"
        
        mail_subject = 'orgaGPS - Activate your account'
        message = (
            f"Hello {user.username},\n\n"
            f"Thank you for registering at orgaGPS! Please activate your account by clicking on the following link:\n"
            f"{activation_link}\n\n"
            "If you didn't request this, please ignore this email.\n\n"
            "Best regards,\nThe orgaGPS Team"
        )

        to_email = serializer.validated_data['email']
        email = EmailMessage(mail_subject, message, to=[to_email])
        try:
            email.send()
        except Exception as e:
            return Response({"error": "Failed to send activation email. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Account-Aktivierung
class ActivateAccountView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid UID or Token"}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({"message": "Account is already activated"}, status=status.HTTP_200_OK)

        # Token wird zusammen mit Ablaufzeit geprüft
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response({"message": "Account activated successfully"})
        
        return Response({"error": "Activation link is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)


# Benutzer erstellen
class CreateUserView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]  # Offen für die erste Registrierung des `product_owner`

    def perform_create(self, serializer):
        # Benutzer wird inaktiv erstellt
        user = serializer.save(is_active=False)

        # Aktivierungslink generieren
        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = f"http://{current_site.domain}/activate?uid={uid}&token={token}"
        
        # Bestätigungs-E-Mail senden
        mail_subject = 'orgaGPS - Activate your account'
        message = (
            f"Hello {user.username},\n\n"
            f"Thank you for registering at orgaGPS! Please activate your account by clicking the following link:\n"
            f"{activation_link}\n\n"
            "If you didn't request this, please ignore this email.\n\n"
            "Best regards,\nThe orgaGPS Team"
        )

        email = EmailMessage(mail_subject, message, to=[user.email])
        try:
            email.send()
        except Exception as e:
            return Response(
                {"error": "Failed to send activation email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CreateUserWithPermissionsView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAdminUser]  # Nur für `product_owner` verfügbar

    def perform_create(self, serializer):
        # Benutzer erstellen und als inaktiv speichern
        email = serializer.validated_data['email']
        new_user = serializer.save(email=email, is_active=False, product_owner=False)

        # Berechtigungen festlegen (diese Informationen kommen aus dem Request)
        permissions_data = self.request.data.get('permissions', {})
        Permissions.objects.create(
            user=new_user,
            can_add_customuser=permissions_data.get('can_add_customuser', False),
            can_edit_customuser=permissions_data.get('can_edit_customuser', False),
            can_delete_customuser=permissions_data.get('can_delete_customuser', False),
            can_add_locations=permissions_data.get('can_add_locations', False),
            can_edit_locations=permissions_data.get('can_edit_locations', False),
            can_delete_locations=permissions_data.get('can_delete_locations', False),
            can_add_schedule=permissions_data.get('can_add_schedule', False),
            can_edit_schedule=permissions_data.get('can_edit_schedule', False),
            can_delete_schedule=permissions_data.get('can_delete_schedule', False),
        )

        # Passwort-Reset-Token und UID generieren
        token = PasswordResetTokenGenerator().make_token(new_user)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))

        # Passwort-Reset-Link generieren
        current_site = get_current_site(self.request)
        reset_link = f"http://{current_site.domain}{reverse('password_reset_confirm')}?uid={uid}&token={token}"

        # E-Mail mit dem Passwort-Reset-Link senden
        mail_subject = 'Welcome to orgaGPS - Set up your password'
        message = (
            f"Hello,\n\n"
            f"Your account has been created successfully. Please set up your password by clicking the link below:\n"
            f"{reset_link}\n\n"
            "Best regards,\nThe orgaGPS Team"
        )

        email = EmailMessage(mail_subject, message, to=[email])
        try:
            email.send()
        except Exception as e:
            return Response(
                {"error": "Failed to send setup email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class EditUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserInfosSerializer
    permission_classes = [CanEditUser]  # Prüft die Berechtigung can_edit_customuser

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return CustomUser.objects.get(pk=user_id)


class DeleteUserView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [CanDeleteUser]  # Prüft die Berechtigung can_delete_customuser

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return CustomUser.objects.get(pk=user_id)


class PasswordResetRequestView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        # Benutzer mit der angegebenen E-Mail-Adresse suchen
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User with this email address does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        current_site = get_current_site(request)
        reset_link = f"http://{current_site.domain}{reverse('password_reset_confirm')}?uid={uid}&token={token}"
        
        mail_subject = "Password Reset Request for OrgaGPS"
        message = (
            f"Hello,\n\n"
            f"Please click the link below to reset your password:\n{reset_link}\n\n"
            "If you didn't request this, please ignore this email.\n\n"
            "Best regards,\nThe OrgaGPS Team"
        )
        
        email = EmailMessage(mail_subject, message, to=[user.email])
        try:
            email.send()
        except Exception as e:
            return Response(
                {"error": "Failed to send password reset email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(
            {"message": "Password reset link has been sent to your email."},
            status=status.HTTP_200_OK
        )
    
# Passwort tatsächlich zurücksetzen
class PasswordResetConfirmView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    
class UserInfosView(generics.UpdateAPIView):
    serializer_class = UserInfosSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user 