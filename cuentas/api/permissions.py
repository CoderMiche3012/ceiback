from rest_framework import permissions

class EsAdminODueno(permissions.BasePermission):
    """
    Permite que un usuario edite un perfil SOLO SI:
    1. Es el Súper Admin de Django.
    2. Tiene el rol de 'Administrador' en la base de datos.
    3. Es el dueño de su propio perfil.
    """
    
    def has_object_permission(self, request, view, obj):
        # 1. Si es el Súper Admin (Tú), lo dejamos pasar a cualquier perfil
        if request.user.is_superuser:
            return True
            
        # 2. Si tiene el rol de Administrador, también lo dejamos pasar a cualquier perfil
        if request.user.id_rol and request.user.id_rol.nombre_rol == 'Administrador':
            return True
            
        # 3. Si es un usuario normal, SOLO pasa si el ID del perfil que intenta editar 
        # es exactamente igual a su propio ID de usuario logueado.
        return obj.id_usuario == request.user.id_usuario