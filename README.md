# 🎾 Club de Tenis Valga — Full-Stack Web App

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL_15-4169E1?style=flat&logo=postgresql&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat&logo=nodedotjs&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat&logo=jsonwebtokens&logoColor=white)

Aplicación web full-stack para la gestión del ranking del **Club de Tenis Valga**. Arquitectura de tres servicios orquestados con Docker Compose, panel de administración protegido con JWT y base de datos PostgreSQL.

---

## 🏗️ Arquitectura

El sistema se despliega en tres contenedores sincronizados mediante **Docker Compose**:

| Contenedor | Tecnología | Responsabilidad |
| :--- | :--- | :--- |
| `ctvalga_db` | PostgreSQL 15 | Persistencia de jugadores, rankings y admins |
| `ctvalga_backend` | FastAPI / Python | Lógica de negocio, JWT, importación de Excel |
| `ctvalga_frontend` | Node.js / Express | Servidor web, logs de acceso, API de clima |

---

## 🛡️ Seguridad

- **Bcrypt**: las contraseñas se almacenan como hashes irreversibles, nunca en texto plano.
- **JWT**: el panel de administración emite tokens firmados con expiración automática.
- **Variables de entorno**: toda la configuración sensible se gestiona mediante `.env`.

---

## 🚀 Instalación

### 1. Prerrequisitos

- [Docker](https://docs.docker.com/get-docker/) y Docker Compose v2.0+

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y rellena tus valores:

```bash
cp .env.example .env
```

### 3. Levantar la infraestructura

```bash
docker compose up -d --build
```

### 4. Importar datos y crear el administrador

```bash
# Importar el ranking desde Excel
docker exec -it ctvalga_backend python /app/scripts/import_ranking.py

# Crear o resetear el administrador (usa las credenciales de tu .env)
docker exec -it ctvalga_backend python /app/scripts/create_admin.py
```

---

## 📂 Estructura del Proyecto

```plaintext
CTVALGA/
├── docker-compose.yml     # Orquestador de servicios
├── .env.example           # Plantilla de variables de entorno
├── backend-api/           # FastAPI + JWT + Bcrypt
├── node-server/
│   └── public/            # Frontend (HTML, CSS, JS)
│       ├── css/
│       ├── js/
│       └── assets/
└── scripts/               # Scripts de inicialización y datos
```

---

## 📍 Puntos de Acceso

| Servicio | URL | Acceso |
| :--- | :--- | :--- |
| Web / Ranking | `http://localhost:3000` | Público |
| Panel Admin | `http://localhost:3000/login.html` | Restringido |
| Docs API | `http://localhost:8000/docs` | Desarrollador |

---

## 🔧 Comandos Útiles

| Acción | Comando |
| :--- | :--- |
| Ver logs en vivo | `docker compose logs -f` |
| Detener todo | `docker compose down` |
| Reconstruir tras cambios | `docker compose up -d --build` |

> Si cambias CSS o JS estáticos, fuerza recarga con `Ctrl + F5` en el navegador.

---

**© 2026 Club de Tenis Valga.** Desarrollado por **Pablo Pérez**. 🎾