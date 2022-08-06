from rest_framework import permissions


""" Permitir al usuario editar su propio perfil """

class UpdateOwnProfile(permissions.BasePermission):
    
    # Chequear si el usuario está intentando editar su propio perfil
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.id == request.user.id)
    
""" Permite actualizar propio status feed """
class UpdateOwnStatus(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Chequear si el usuario está intentando entrar a su propio perfil
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile_id == request.user.id