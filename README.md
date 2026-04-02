
```markdown
# Backend CEI - Sprint 1: Seguridad y Accesos 🛡️

Este proyecto contiene el backend del Sistema Integral para el Centro de Esperanza Infantil A.C. (CEI). Este primer sprint implementa una base de datos relacional normalizada, validaciones de seguridad mediante expresiones regulares, un modelo de usuario personalizado y autenticación basada en JSON Web Tokens (JWT).

## 🛠️ Tecnologías Utilizadas
* Python 3
* Django & Django REST Framework (DRF)
* PostgreSQL (vía Docker)
* SimpleJWT (Autenticación)

---

## 🚀 Guía de Instalación y Configuración Local

Sigue estos pasos en orden para levantar el proyecto desde cero en un entorno local (instrucciones para Windows PowerShell).

### 1. Entorno Virtual
Crea un espacio aislado para instalar las dependencias sin afectar tu sistema global:
```powershell
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
.\venv\Scripts\Activate
```

### 2. Gestión de Paquetes y Librerías
Con el entorno activado `(venv)`, actualiza el gestor de paquetes e instala las librerías necesarias para que el proyecto funcione:
```powershell
# Actualizar pip a la última versión
python.exe -m pip install --upgrade pip

# Cargar las librerías en colaborativo desde el archivo de requerimientos
pip install -r requirements.txt
```

*(Nota para el equipo de desarrollo: Si instalas una librería nueva en el futuro, recuerda guardarla ejecutando: `pip freeze > requirements.txt`)*

### 3. Comandos Base de Django (Referencia)
Estos son los comandos que se utilizaron para iniciar la estructura, útiles si se requiere escalar el sistema creando nuevos módulos:
```powershell
# Iniciar un proyecto nuevo (Ya realizado)
django-admin startproject config .

# Crear una nueva aplicación dentro del proyecto (Ya realizado para la app 'cuentas')
python manage.py startapp nombre_de_la_app
```

### 4. Base de Datos y Migraciones
Asegúrate de tener tu base de datos PostgreSQL conectada (o el contenedor de Docker encendido). Luego, sincroniza los modelos con las tablas de la BD:
```powershell
# Preparar los archivos de migración si hubo cambios en los modelos
python manage.py makemigrations

# Aplicar los cambios y crear las tablas en PostgreSQL
python manage.py migrate
```

### 5. Poblar la Base de Datos Inicial
Ejecuta el script de automatización para crear la matriz estática de roles y permisos del sistema (Administrador, Trabajadora Social, etc.) para que React pueda consumirlos:
```powershell
# Crear roles y permisos automáticamente
python manage.py setup_roles
```

### 6. Crear el Superusuario (Administrador)
Para acceder al panel de control integrado de Django, utiliza este comando y crea tu cuenta maestra:
```powershell
python manage.py createsuperuser
```
**Credenciales de acceso inicial sugeridas para pruebas:**
* **Nom usuario:** `admin`
* **Correo:** `admin2026@gmail.com`
* **Nombre:** `admin`
* **Apellido p:** `cei`
* **Password:** `admin123456-`

### 7. Levantar el Servidor
Finalmente, enciende el servidor de desarrollo:
```powershell
python manage.py runserver
```
El panel de administración estará disponible en: `http://127.0.0.1:8000/admin/`

---

## 🔌 Directorio de la API (Endpoints)

Todas las rutas base para el frontend comienzan con: `http://127.0.0.1:8000/`

### Autenticación (JWT)
| Método | Ruta | Descripción | Requiere Token |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/cuentas/login/` | Recibe `nom_usuario` y `password` en JSON. Devuelve los tokens `access` y `refresh`. | ❌ No |
| **POST** | `/api/cuentas/login/refresh/` | Recibe el token de `refresh` y devuelve un nuevo token de `access`. | ❌ No |

### Gestión de Usuarios
| Método | Ruta | Descripción | Requiere Token |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/cuentas/registro/` | Crea un nuevo usuario validando datos estrictamente. | ❌ No |
| **GET** | `/api/cuentas/usuarios/` | Lista todos los usuarios registrados en el sistema. | ✅ Sí |
| **GET** | `/api/cuentas/usuarios/{id}/` | Detalles específicos de un usuario por su ID. | ✅ Sí |
| **PUT/PATCH**| `/api/cuentas/usuarios/{id}/` | Actualiza la información de un usuario. | ✅ Sí |
| **DELETE** | `/api/cuentas/usuarios/{id}/` | Elimina a un usuario. | ✅ Sí |

### 📚 Configuración Escolar (Sprint 2)
| Método | Ruta | Descripción | Requiere Token |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/periodos/periodos/` | Lista todos los periodos y ciclos escolares. | ✅ Sí |
| **POST** | `/api/periodos/periodos/` | Crea un nuevo periodo (Valida formato YYYY-YYYY). | ✅ Sí |
| **PUT/DELETE** | `/api/periodos/periodos/{id}/` | Modifica o elimina un periodo específico. | ✅ Sí |

### 🧾 1. Flujo de Postulación (App Beneficiarios)
| Método | Ruta | Descripción | Requiere Token |
| :--- | :--- | :--- | :--- |
| **GET/POST** | `/api/beneficiarios/direcciones/` | Gestiona las direcciones físicas. | ✅ Sí |
| **GET/POST** | `/api/beneficiarios/expedientes/` | Gestiona los expedientes base (Datos personales + id_direccion). | ✅ Sí |
| **GET/POST** | `/api/beneficiarios/postulantes/` | Ruta maestra: crea Dirección, Expediente y Postulante desde JSON anidado. | ✅ Sí |
| **GET/POST** | `/api/beneficiarios/visitas/` | Agenda y gestiona las visitas domiciliarias de los postulantes. | ✅ Sí |

### 📊 2. Estudio Socioeconómico (App Estudios)
| Método | Ruta | Descripción | Requiere Token |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/estudios/estudios/` | Obtiene la lista de estudios socioeconómicos realizados. | ✅ Sí |
| **POST** | `/api/estudios/estudios/` | Ruta maestra: guarda Estudio, Familia, Vivienda, Gastos, Alimentación y Análisis. | ✅ Sí |
| **GET/PUT** | `/api/estudios/estudios/{id}/` | Consulta o actualiza un estudio socioeconómico específico. | ✅ Sí |

### ✅ 3. Aceptación Final
| Método | Ruta | Descripción | Requiere Token |
| :--- | :--- | :--- | :--- |
| **GET/POST** | `/api/beneficiarios/beneficiarios/` | Convierte a un candidato en Beneficiario Oficial (usa id_expediente). | ✅ Sí |
| **PUT/DELETE** | `/api/beneficiarios/beneficiarios/{id}/` | Gestiona el estatus y notas del beneficiario activo. | ✅ Sí |

### Roles y Permisos (Catálogos)
| Método | Ruta | Descripción | Requiere Token |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/cuentas/roles/` | Devuelve la lista estática de Roles (para selectores en React). | ❌ No |
| **GET** | `/api/cuentas/permisos/` | Devuelve la matriz completa de permisos disponibles. | ❌ No |

> **Importante para el Frontend:** Para las peticiones que requieren token (✅), se debe incluir en las cabeceras HTTP de la petición (fetch/axios) lo siguiente:
> `Authorization: Bearer <token_access_generado>`
```
