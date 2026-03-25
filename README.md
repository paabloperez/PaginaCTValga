# 🎾 Club de Tenis Valga - Sistema de Gestión Full-Stack

¡Bienvenido! Esta es una aplicación profesional diseñada para la gestión del ranking y la visualización de datos en tiempo real del **Club de Tenis Valga**. 

El proyecto utiliza una arquitectura moderna de microservicios: un backend de datos en **Python**, un servidor intermedio de aplicaciones en **Node.js** y un frontend dinámico.

---

## 🏗️ Arquitectura del Sistema

El proyecto está dividido en tres capas independientes:

1. **Backend API (Python/FastAPI)**: Gestiona la lógica de negocio, la conexión a **PostgreSQL** y sirve los datos del ranking.
2. **Node Server (Node.js/Express)**: Actúa como servidor web principal, consume APIs externas (Clima), gestiona logs de acceso y sirve los archivos estáticos.
3. **Frontend (HTML5/CSS3/JS)**: Interfaz de usuario *responsive* que consume datos de ambas capas de backend.

---

## 🚀 Guía de Configuración Rápida

### 1. Requisitos Previos
* **PostgreSQL** instalado y con una base de datos llamada `clubtenis_db`.
* **Python 3.10+** y **Node.js 18+** instalados.

### 2. Configuración del Backend (Python)
Desde la carpeta `backend-api/`:

```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env  # Edita el archivo .env con tus credenciales de Postgres

# Importar datos iniciales desde Excel (opcional)
python ../scripts/import_ranking.py

# Iniciar el servidor de datos
uvicorn main:app --reload
```
> 📍 **API disponible en:** `http://localhost:8000/docs`

### 3. Configuración del Servidor Web (Node.js)
Desde la carpeta `node-server/`:

```bash
# Instalar dependencias
npm install

# Iniciar el servidor web
node app.js
```
> 📍 **Web principal disponible en:** `http://localhost:3000`

---

## 📂 Estructura del Proyecto

```plaintext
CTVALGA/
├── backend-api/        # API REST en FastAPI y modelos de PostgreSQL.
├── node-server/        # Servidor Express.js y Middleware.
│   ├── public/         # Frontend: HTML, CSS, JS e imágenes.
│   └── accesos.txt     # Logs automáticos de actividad.
├── scripts/            # Utilidades de procesamiento de datos (Pandas/Excel).
└── .gitignore          # Exclusión de entornos virtuales y node_modules.
```

---

## 🛠️ Tecnologías Utilizadas

| Capa | Tecnologías |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Grid/Flexbox), JavaScript Moderno (Fetch API) |
| **Backend App** | Node.js, Express.js, CORS |
| **Backend Data** | Python, FastAPI, SQLAlchemy, Pydantic |
| **Base de Datos** | PostgreSQL |
| **Data Tools** | Pandas, Openpyxl (para ingesta de archivos .xlsx) |
| **APIs Externas** | Open-Meteo (Previsión meteorológica en Valga) |

---

## 💡 Notas para Colaboradores

* **Seguridad:** Nunca subas el archivo `.env` al repositorio. Usa `.env.example` como plantilla.
* **Logs:** El servidor Node registra automáticamente cada visita en `node-server/accesos.txt`.
* **CORS:** El sistema está configurado para permitir peticiones entre el puerto **3000** y el **8000**.

---

**© 2026 Club de Tenis Valga.** Desarrollado por **Pablo Pérez**.
```

¿Necesitas que te ayude a redactar también el archivo `.gitignore` o el `.env.example` para que el repositorio quede redondo?