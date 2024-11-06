# accounts/permissions.py

from rest_framework.permissions import BasePermission

class CanAddUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.permissions.can_add_customuser

class CanEditUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.permissions.can_edit_customuser

class CanDeleteUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.permissions.can_delete_customuser
