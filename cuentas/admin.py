from django.contrib import admin
from .models import Usuario, Rol, Permiso

# Estas clases le dicen a Django qué columnas mostrar en la tablita del panel
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nom_usuario', 'nombre', 'apellido_p', 'correo', 'id_rol', 'estatus')
    search_fields = ('nom_usuario', 'correo', 'nombre')
    list_filter = ('estatus', 'id_rol')

class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre_rol', 'descripcion')
    search_fields = ('nombre_rol',)

class PermisoAdmin(admin.ModelAdmin):
    list_display = ('nombre_permiso', 'descripcion')

# Aquí registramos tus modelos para que aparezcan en el panel
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol, RolAdmin)
admin.site.register(Permiso, PermisoAdmin)