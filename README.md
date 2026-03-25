# 🎾 Club de Tenis Valga - Sistema de Gestión Full-Stack (Docker Edition)

¡Bienvenido! Esta es una aplicación profesional diseñada para la gestión del ranking y la visualización de datos en tiempo real del **Club de Tenis Valga**. 

El proyecto utiliza una arquitectura moderna de microservicios totalmente **contenedorizada con Docker**, garantizando que el sistema funcione en cualquier entorno sin necesidad de configurar bases de datos o entornos virtuales manualmente.

---

## 🏗️ Arquitectura del Sistema (Microservicios)

El sistema se despliega mediante **Docker Compose** en tres contenedores independientes que se comunican a través de una red interna privada:

1.  **`db` (PostgreSQL 15)**: Base de datos relacional para la persistencia de jugadores y rankings.
2.  **`backend` (Python/FastAPI)**: API REST que gestiona la lógica de negocio, modelos de SQLAlchemy y comunicación con la DB.
3.  **`frontend-server` (Node.js/Express)**: Servidor web principal, gestor de logs de acceso, puente con la API de clima y servidor de archivos estáticos.

---

## 🚀 Guía de Configuración Rápida (Docker)

La principal ventaja de esta arquitectura es la simplicidad. Solo necesitas tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### 1. Levantar la infraestructura
Desde la raíz del proyecto `CTValga/`, ejecuta:

```bash
# Construir las imágenes y levantar los servicios en segundo plano
docker-compose up -d --build
```

### 2. Inicializar la Base de Datos (Primer inicio)
Como la base de datos nace limpia, debemos crear la estructura e importar los datos del ranking:

```bash
# A. Crear las tablas necesarias en Postgres
docker exec -it ctvalga_db_1 psql -U user_valga -d clubtenis_db -c "
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    licencia VARCHAR(20) UNIQUE NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    club_federacion VARCHAR(255),
    categoria VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS ranking_entry (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    puntos INTEGER,
    posicion_global INTEGER,
    posicion_club INTEGER,
    fecha_ranking DATE,
    UNIQUE(player_id, fecha_ranking)
);"

# B. Importar datos desde el archivo Excel
docker cp ./scripts/import_ranking.py ctvalga_backend_1:/app/import_ranking.py
docker cp ./scripts/ranking_M.xlsx ctvalga_backend_1:/app/ranking_M.xlsx
docker exec -it ctvalga_backend_1 python import_ranking.py
```

---

## 📍 Puntos de Acceso

| Servicio | URL Local | Descripción |
| :--- | :--- | :--- |
| **Web Principal** | `http://localhost:3000` | Interfaz de usuario y Ranking |
| **Documentación API** | `http://localhost:8000/docs` | Swagger UI interactivo de FastAPI |
| **API Clima** | `http://localhost:3000/api/clima` | Endpoint de meteorología (Node) |

---

## 📂 Estructura del Proyecto

```plaintext
CTVALGA/
├── docker-compose.yml   # Orquestador de contenedores.
├── backend-api/         # Microservicio Python (FastAPI).
│   ├── Dockerfile
│   └── main.py
├── node-server/         # Microservicio Node.js (Express).
│   ├── Dockerfile
│   ├── app.js
│   └── public/          # Frontend: HTML, CSS y JS.
├── scripts/             # Scripts de utilidad (Pandas/Excel).
└── .env                 # Variables de entorno configuradas para Docker.
```

---

## 🛠️ Tecnologías Utilizadas

| Capa | Tecnologías |
| :--- | :--- |
| **Orquestación** | Docker, Docker Compose |
| **Frontend** | HTML5, CSS3, JavaScript (Fetch API) |
| **Servidor App** | Node.js, Express.js, CORS |
| **API de Datos** | Python 3.10, FastAPI, SQLAlchemy |
| **Base de Datos** | PostgreSQL 15 |
| **Procesamiento** | Pandas, Openpyxl |

---

## 💡 Comandos de Mantenimiento

* **Ver estado de servicios**: `docker ps`
* **Ver logs del backend**: `docker logs -f ctvalga_backend_1`
* **Pausar el club (Mantiene datos)**: `docker-compose stop`
* **Reiniciar servicios**: `docker-compose restart`
* **Borrar infraestructura**: `docker-compose down` (Cuidado: borra la BD si no hay volúmenes).

---

**© 2026 Club de Tenis Valga.** Desarrollado por **Pablo Pérez**.
```