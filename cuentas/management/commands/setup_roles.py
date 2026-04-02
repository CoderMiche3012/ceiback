from django.core.management.base import BaseCommand
from cuentas.models import Rol, Permiso

class Command(BaseCommand):
    help = 'Crea los roles y permisos estáticos iniciales del sistema CEI'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando la configuración de roles y permisos...")


        modulos = ['Beneficiarios', 'Donadores', 'Postulantes', 'Cursos', 'Reportes',
                    'Usuarios', 'Roles', 'Permisos', 'Periodos']
        acciones = ['Ver', 'Crear', 'Editar', 'Eliminar']

        #permisos 
        permisos_creados = {}
        for modulo in modulos:
            for accion in acciones:
                nombre = f"{accion} {modulo}"
                permiso, created = Permiso.objects.get_or_create(
                    nombre_permiso=nombre,
                    defaults={'descripcion': f'Permite {accion.lower()} información en el módulo de {modulo}'}
                )
                permisos_creados[nombre] = permiso

        self.stdout.write(self.style.SUCCESS(f'Se verificaron/crearon {len(permisos_creados)} permisos.'))

        # 3. Crear los Roles de tu diseño
        roles_data = [
            {'nombre': 'Administrador', 'desc': 'Acceso total al sistema'},
            {'nombre': 'Trabajadora Social', 'desc': 'Gestión de beneficiarios'},
            {'nombre': 'Coordinación', 'desc': 'Supervisión y reportes'},
            {'nombre': 'Mesa Directiva', 'desc': 'Sólo lectura y auditoría'},
        ]

        for rol_data in roles_data:
            rol, created = Rol.objects.get_or_create(
                nombre_rol=rol_data['nombre'],
                defaults={'descripcion': rol_data['desc']}
            )
            
            # 4. Asignar permisos según el rol
            if rol.nombre_rol == 'Administrador':
                # El admin recibe TODOS los permisos
                rol.permisos.set(permisos_creados.values())
                
            elif rol.nombre_rol == 'Mesa Directiva':
                # Solo permisos de "Ver"
                permisos_lectura = [p for nombre, p in permisos_creados.items() if nombre.startswith('Ver')]
                rol.permisos.set(permisos_lectura)
                
            # Puedes ir agregando los 'elif' para configurar exactamente qué permisos 
            # lleva la Trabajadora Social, Coordinación, etc.

            self.stdout.write(self.style.SUCCESS(f'Rol configurado: {rol.nombre_rol}'))

        self.stdout.write(self.style.SUCCESS('¡Configuración de BD completada con éxito!'))