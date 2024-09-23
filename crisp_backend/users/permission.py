from rest_framework import permissions
from .utils import get_account_type

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_account_type(request.user) == 'SuperAdmin'
    
class IsDepartmentAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_account_type(request.user) == 'DepartmentAdmin'
    
class IsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_account_type(request.user) == 'Worker'
    
class IsCitizen(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_account_type(request.user) == 'Citizen'