# accounts/urls.py

from django.urls import path
from .views import RegisterUserView, ActivateAccountView, CreateUserView, CustomTokenObtainPairView, PasswordResetRequestView, PasswordResetConfirmView, CreateUserWithPermissionsView, EditUserView, DeleteUserView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/accounts/register/', RegisterUserView.as_view(), name='register'),
    path('api/accounts/activate/', ActivateAccountView.as_view(), name='activate'),
    path('api/accounts/create-user/', CreateUserView.as_view(), name='create_user'),
    path('api/accounts/create-user-with-permissions/', CreateUserWithPermissionsView.as_view(), name='create_user_with_permissions'),
    path('api/accounts/edit-user/<int:pk>/', EditUserView.as_view(), name='edit_user'),
    path('api/accounts/delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('api/accounts/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/accounts/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
