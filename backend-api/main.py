from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import date

# --- 1. CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_CONFIG = {
    'dbname': 'clubtenis_db',
    'user': 'postgres',
    'password': 'REDACTED',
    'host': 'localhost',
    'port': '5432'
}

# --- 2. DEFINICIÓN DEL MODELO DE DATOS (Pydantic) ---
# Esto asegura que la respuesta de tu API tenga un formato claro.
class RankingEntry(BaseModel):
    id: int
    licencia: str
    nombre_completo: str
    puntos: int
    posicion_global: Optional[int] = None
    posicion_club: Optional[int] = None
    categoria: str
    fecha_ranking: date

# --- 3. INICIALIZACIÓN DE LA APLICACIÓN ---
app = FastAPI()

# --- 4. FUNCIÓN DE CONEXIÓN A DB ---
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error de conexión a PostgreSQL: {e}")
        # En una aplicación real, no harías esto, pero aquí ayuda a depurar.
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos.")

# --- 5. RUTA PRINCIPAL DE LA API ---
@app.get("/api/ranking", response_model=List[RankingEntry])
def read_ranking():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta SQL que combina jugadores y su último ranking
    # Seleccionamos la entrada de ranking más reciente de cada jugador
    query = """
    SELECT
        p.id, p.licencia, p.nombre_completo, re.puntos,
        re.posicion_global,
        re.posicion_club,
        p.categoria, re.fecha_ranking
    FROM players p
    JOIN ranking_entry re ON p.id = re.player_id
    WHERE re.fecha_ranking = (SELECT MAX(fecha_ranking) FROM ranking_entry)
    ORDER BY re.puntos DESC;
    """
    
    try:
        cursor.execute(query)
        # Obtenemos los nombres de las columnas para crear diccionarios
        column_names = [desc[0] for desc in cursor.description]
        
        # Mapeamos los resultados de la DB a una lista de diccionarios (JSON)
        results = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        
        return results
    except Exception as e:
        print(f"Error al ejecutar consulta: {e}")
        raise HTTPException(status_code=500, detail="Error al recuperar datos del ranking.")
    finally:
        cursor.close()
        conn.close()

# --- 6. Habilitar CORS para permitir conexión desde Next.js ---
# Esto es necesario en desarrollo. Descomenta si tienes problemas.
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:5500",      # Puerto común para Live Server (HTML/JS)
    "http://127.0.0.1:5500",      # Alternativa para Live Server
    "http://localhost:3000",]     # Permite cualquier origen en desarrollo, por si vuelvo a next.js, no tiene pinta

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#para que esto funcione:
# desde scripts activar el entorno con source venv/bin/activate y desde backend-api correr uvicorn main:app --reload
# Luego acceder a http://127.0.0.1:8000/docs para ver la documentación automática de la API.
#luego npm run dev en el frontend y acceder a http://localhost:3000/ranking