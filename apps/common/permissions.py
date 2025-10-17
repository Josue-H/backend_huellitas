from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permiso para usuarios administradores autenticados
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsSuperAdmin(permissions.BasePermission):
    """
    Permiso solo para super administradores
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'super_admin'
        )


class CanManagePets(permissions.BasePermission):
    """
    Permiso para gestionar mascotas
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Roles que pueden gestionar mascotas
        allowed_roles = ['super_admin', 'admin', 'volunteer', 'veterinarian']
        return request.user.role in allowed_roles


class CanManageAdoptions(permissions.BasePermission):
    """
    Permiso para gestionar adopciones
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Roles que pueden gestionar adopciones
        allowed_roles = ['super_admin', 'admin', 'volunteer']
        return request.user.role in allowed_roles


class CanManageContent(permissions.BasePermission):
    """
    Permiso para gestionar contenido (noticias, historias)
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Roles que pueden gestionar contenido
        allowed_roles = ['super_admin', 'admin']
        return request.user.role in allowed_roles


class CanManageUsers(permissions.BasePermission):
    """
    Permiso para gestionar usuarios (solo super_admin)
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'super_admin'
        )