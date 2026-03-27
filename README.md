# 🎾 Club de Tenis Valga - Full-Stack (Docker & JWT Security)

¡Proyecto completado! Esta es una aplicación profesional de alto rendimiento para la gestión del ranking del **Club de Tenis Valga**, diseñada con una arquitectura de microservicios moderna y segura.

---

## 🏗️ Arquitectura del Sistema (Microservicios)

El sistema se despliega mediante **Docker Compose** en tres contenedores sincronizados:

1.  **`ctvalga_db` (PostgreSQL 15)**: Persistencia de datos (Jugadores, Rankings y Admins).
2.  **`ctvalga_backend` (FastAPI/Python)**: El "cerebro" del club. Gestiona la lógica de negocio, importación de Excel y **seguridad JWT (JSON Web Tokens)** con hasheo de contraseñas mediante `bcrypt`.
3.  **`ctvalga_frontend` (Node.js/Express)**: Servidor web que sirve la interfaz, gestiona logs de acceso y conecta con la API de clima externa.



---

## 🛡️ Seguridad y Administración

El sistema incluye una **Capa de Seguridad Industrial**:
* **Hasheo Bcrypt**: Las contraseñas nunca se guardan en texto plano; se transforman en hashes irreversibles en la base de datos.
* **Tokens JWT**: El panel de administración emite "pasaportes digitales" firmados que caducan automáticamente.
* **Validación de Sesión**: La interfaz reconoce al administrador y personaliza la experiencia (saludo dinámico y botones de sesión).

---

## 🚀 Guía de Configuración Rápida

### 1. Levantar la infraestructura
```bash
# Construir y levantar todo el ecosistema
docker compose up -d --build
```

### 2. Importar Datos y Crear Admin
```bash
# Importar el ranking desde el Excel
docker exec -it ctvalga_backend python /app/scripts/import_ranking.py

# (Opcional) Crear/Resetear el Administrador
# Usuario: perez_admin | Pass: REDACTED
docker exec -it ctvalga_backend python -c "import psycopg2, bcrypt, os; conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT')); cur = conn.cursor(); hashed = bcrypt.hashpw(b'REDACTED', bcrypt.gensalt()).decode(); cur.execute('DELETE FROM admins WHERE username = \'perez_admin\''); cur.execute('INSERT INTO admins (username, password_hash) VALUES (%s, %s)', ('perez_admin', hashed)); conn.commit(); print('✅ Admin configurado')"
```

---

## 📂 Estructura Final del Proyecto

```plaintext
CTVALGA/
├── docker-compose.yml     # Orquestador de servicios.
├── backend-api/           # Lógica FastAPI + Seguridad JWT + Bcrypt.
├── node-server/
│   └── public/            # Frontend (HTML, CSS, JS).
│       ├── css/           # Estilos (styles.css, login.css).
│       ├── js/            # Lógica (login.js, ranking dinámico).
│       └── assets/        # Imágenes y Logos.
└── scripts/               # Volumen persistente (Excel, SQL, Logs).
```

---

## 📍 Puntos de Acceso

| Servicio | URL Local | Acceso |
| :--- | :--- | :--- |
| **Web / Ranking** | `http://localhost:3000` | Público |
| **Panel Admin** | `http://localhost:3000/login.html` | Restringido |
| **Docs API** | `http://localhost:8000/docs` | Desarrollador |

---

## 💡 Comandos de Emergencia

* **¿Algo no carga?** Revisa logs: `docker compose logs -f`
* **¿Cambiaste el CSS/JS?** Pulsa `Ctrl + F5` en el navegador.
* **¿Quieres apagarlo todo?** `docker compose down` (Tus datos seguirán a salvo).

---

**© 2026 Club de Tenis Valga.** Desarrollado por **Pablo Pérez**. 🎾🏆
