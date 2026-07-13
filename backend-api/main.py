import os
from datetime import datetime, timedelta, date, timezone
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from jose import JWTError, jwt
import bcrypt

load_dotenv()

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- 2. CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# --- 3. MODELOS DE DATOS ---
class RankingEntry(BaseModel):
    id: int
    licencia: str
    nombre_completo: str
    puntos: int
    posicion_global: Optional[int] = None
    posicion_club: Optional[int] = None
    categoria: str
    fecha_ranking: date

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- 4. INICIALIZACIÓN ---
app = FastAPI()

# --- 5. CORS ---
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 6. FUNCIONES DE UTILIDAD ---
def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print(f"Error de conexión: {e}")
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos.")

def verify_password(plain_password, hashed_password):
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- 7. ENDPOINTS ---

@app.post("/api/login", response_model=Token)
def login(login_data: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT username, password_hash FROM admins WHERE username = %s"
        cursor.execute(query, (login_data.username,))
        admin = cursor.fetchone()

        if not admin or not verify_password(login_data.password, admin[1]):
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

        access_token = create_access_token(data={"sub": admin[0]})
        return {"access_token": access_token, "token_type": "bearer"}

    finally:
        cursor.close()
        conn.close()

@app.get("/api/ranking", response_model=List[RankingEntry])
def read_ranking():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        p.id, p.licencia, p.nombre_completo, re.puntos,
        re.posicion_global, re.posicion_club,
        p.categoria, re.fecha_ranking
    FROM players p
    JOIN ranking_entry re ON p.id = re.player_id
    WHERE re.fecha_ranking = (SELECT MAX(fecha_ranking) FROM ranking_entry)
    ORDER BY re.puntos DESC;
    """

    try:
        cursor.execute(query)
        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        return results
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al recuperar ranking.")
    finally:
        cursor.close()
        conn.close()