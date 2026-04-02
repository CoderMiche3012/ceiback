from rest_framework import permissions

class EsAdminODueno(permissions.BasePermission):
    # ... (Este se queda exactamente igual, no le muevas nada) ...
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.id_rol and request.user.id_rol.nombre_rol == 'Administrador':
            return True
        return obj.id_usuario == request.user.id_usuario


class EsAdmin(permissions.BasePermission):
    """
    Permiso exclusivo para catálogos globales como Roles y Permisos.
    SOLO el Súper Admin o el rol 'Administrador' pueden ver, agregar, editar o eliminar.
    """
    
    def has_permission(self, request, view):
        # 1. Protege la lista general (GET general) y la creación (POST)
        if not request.user or not request.user.is_authenticated:
            return False
        
        es_super = request.user.is_superuser
        es_admin = request.user.id_rol and request.user.id_rol.nombre_rol == 'Administrador'
        
        return es_super or es_admin

    def has_object_permission(self, request, view, obj):
        # 2. Protege un rol en específico (GET por ID, PUT, PATCH, DELETE)
        es_super = request.user.is_superuser
        es_admin = request.user.id_rol and request.user.id_rol.nombre_rol == 'Administrador'
        
        return es_super or es_admin