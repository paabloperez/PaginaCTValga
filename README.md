# 🎾 Club de Tenis Valga - Sistema de Ranking

¡Bienvenido al proyecto! Esta es una aplicación web para gestionar el ranking de los jugadores del club. El sistema cuenta con un frontend en HTML/JS y un backend robusto con FastAPI y PostgreSQL.

---

## 🚀 Guía de Configuración Rápida

Sigue estos pasos para tener el proyecto funcionando en tu máquina local:

### 1. Preparar la Base de Datos
* Asegúrate de tener **PostgreSQL** instalado y corriendo.
* Crea una base de datos nueva llamada: `clubtenis_db`.

### 2. Configurar el Entorno Virtual
Desde la terminal, en la raíz del proyecto, ejecuta:
```bash
# Crear el entorno virtual
python -m venv venv

# Activarlo (Windows)
.\venv\Scripts\activate

# Activarlo (Mac/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Variables de Entorno (Seguridad)
Por seguridad, las credenciales no están en el código.
1. Ve a la carpeta `backend-api/`.
2. Crea un archivo llamado `.env`.
3. Usa como base el archivo `.env.example` y rellénalo con tus datos (especialmente tu contraseña de Postgres).

### 4. Carga de Datos Iniciales
Para poblar la base de datos con la información del archivo Excel (asegúrate de tener el archivo `.xlsx` en la carpeta `scripts/`):
```bash
# Desde la raíz del proyecto
python scripts/import_ranking.py
```
### 5. Ejecutar el Servidor API
Para levantar el backend, navega a la carpeta correspondiente y lanza Uvicorn:

```bash
cd backend-api
uvicorn main:app --reload
```
La documentación interactiva de la API (Swagger UI) estará disponible en: http://127.0.0.1:8000/docs

### 📂 Estructura del Proyecto

    frontend/: Archivos de la interfaz (HTML, CSS, JS puro).

    backend-api/: API REST construida con FastAPI y conexión a PostgreSQL.

    scripts/: Scripts de utilidad para la importación de datos desde Excel (.xlsx).

    .gitignore: Configuración para excluir archivos sensibles (.env) y entornos virtuales (venv/).

### 🛠️ Tecnologías utilizadas

    Backend: FastAPI, Psycopg2, Python-dotenv.

    Frontend: JavaScript (ES6+), CSS3, HTML5.

    Base de Datos: PostgreSQL.

    Procesamiento de Datos: Pandas, Openpyxl.

### 💡 Recordatorio para colaboradores

No olvides crear el archivo `.env.example` dentro de `backend-api/` con el siguiente contenido básico para que el sistema pueda conectar a la base de datos:

    DB_NAME=clubtenis_db
    
    DB_USER=postgres
    
    DB_PASSWORD=tu_contraseña_aqui
    
    DB_HOST=localhost
    
    DB_PORT=5432
