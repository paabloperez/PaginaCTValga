# 🎾 Club de Tenis Valga - Sistema de Gestión Full-Stack (Docker Edition)

¡Bienvenido! Esta es una aplicación profesional diseñada para la gestión del ranking y la visualización de datos en tiempo real del **Club de Tenis Valga**. 

El proyecto utiliza una arquitectura moderna de microservicios totalmente **contenedorizada con Docker**, lo que permite desplegar toda la infraestructura (Base de Datos, API y Servidor Web) con un solo comando.

---

## 🏗️ Arquitectura del Sistema (Microservicios)

El sistema se despliega mediante **Docker Compose** en tres contenedores independientes:

1.  **`ctvalga_db` (PostgreSQL 15)**: Base de datos persistente. Se inicializa automáticamente con el esquema de tablas.
2.  **`ctvalga_backend` (Python/FastAPI)**: API REST que gestiona la lógica de negocio y el procesamiento de datos.
3.  **`ctvalga_frontend` (Node.js/Express)**: Servidor web principal, gestor de logs y puente con la API de clima.

---

## 🚀 Guía de Configuración Rápida (Docker)

### 1. Levantar la infraestructura
Desde la raíz del proyecto `CTValga/`, ejecuta:

```bash
# Construir imágenes y levantar servicios (las tablas se crean solas)
docker compose up -d --build
````

### 2\. Importar Datos del Ranking

Para poblar la base de datos desde el archivo Excel (`scripts/ranking_M.xlsx`), solo necesitas ejecutar el script de importación dentro del contenedor:

```bash
# Ejecutar la importación (Docker ya ve el Excel gracias a los volúmenes)
docker exec -it -w /app/scripts ctvalga_backend python import_ranking.py
```

-----

## 📍 Puntos de Acceso

| Servicio | URL Local | Descripción |
| :--- | :--- | :--- |
| **Web Principal** | [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000) | Interfaz de usuario y Ranking |
| **Documentación API** | [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs) | Swagger UI (FastAPI) |

-----

## 📂 Estructura del Proyecto

```plaintext
CTVALGA/
├── docker-compose.yml   # Orquestador de la infraestructura.
├── backend-api/         # Microservicio Python (FastAPI).
├── node-server/         # Microservicio Node.js (Express) + Frontend.
└── scripts/             # Carpeta persistente (Excel, SQL y Scripts).
    ├── schema.sql       # Script de creación automática de tablas.
    ├── ranking_M.xlsx   # Fuente de datos Excel.
    └── import_ranking.py # Lógica de importación a la DB.
```

-----

## 🛠️ Tecnologías Utilizadas

| Capa | Tecnologías |
| :--- | :--- |
| **Orquestación** | Docker & Docker Compose |
| **Frontend** | HTML5, CSS3, JavaScript (Fetch API) |
| **Servidores** | Node.js (Express), Python (FastAPI) |
| **Persistencia** | PostgreSQL 15 + Docker Volumes |
| **Data Science** | Pandas, Openpyxl |

-----

## 💡 Comandos de Mantenimiento

  * **Ver estado de los contenedores**: `docker ps`
  * **Ver logs en tiempo real**: `docker logs -f ctvalga_backend`
  * **Apagar el sistema (Mantiene datos)**: `docker compose stop`
  * **Borrar todo (Limpieza profunda)**: `docker compose down -v`

-----

**© 2026 Club de Tenis Valga.** Desarrollado por **Pablo Pérez**.