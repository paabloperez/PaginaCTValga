import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import date
from typing import Dict, Any

# ----------------------------------------------------
# A. FUNCIÓN DE CONEXIÓN A LA BASE DE DATOS
# ----------------------------------------------------
def get_db_connection(db_config: Dict[str, Any]):
    """Establece y devuelve la conexión a PostgreSQL."""
    try:
        conn = psycopg2.connect(
            dbname=db_config['db_name'],
            user=db_config['db_user'],
            password=db_config['db_password'],
            host=db_config.get('db_host', 'localhost'),
            port=db_config.get('db_port', '5432')
        )
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# ----------------------------------------------------
# B. FUNCIÓN DE UPSERT DE JUGADORES Y REGISTRO DE RANKING
# ----------------------------------------------------
def upsert_player_and_insert_ranking(conn, row, fecha_ranking):
    """
    Realiza el UPSERT (INSERT o UPDATE) en la tabla players 
    y luego inserta el registro en ranking_entry, utilizando los nombres de columna del Excel.
    Incluye manejo robusto de nombres nulos.
    """
    cursor = conn.cursor()
    licencia = str(row['Licencia'])
    
    # 1. UPSERT en la tabla players
    upsert_query = sql.SQL("""
        INSERT INTO players (licencia, nombre_completo, club_federacion, categoria)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (licencia) DO UPDATE SET
            nombre_completo = EXCLUDED.nombre_completo,
            club_federacion = EXCLUDED.club_federacion,
            categoria = EXCLUDED.categoria
        RETURNING id;
    """)
    
    # --- Manejo robusto de nombre completo (Corrección de errores anteriores) ---
    # Usamos .get para manejar posibles valores faltantes y str().strip() para limpiar.
    nombre = str(row.get('Nombre', '')).strip()
    apellidos = str(row.get('Apellidos', '')).strip()
    nombre_completo = f"{nombre} {apellidos}".strip()

    # Evitar el error de restricción NOT NULL si el nombre es totalmente vacío
    if not nombre_completo:
        nombre_completo = "Nombre Desconocido"
    # --- Fin de Manejo robusto ---
    
    try:
        cursor.execute(
            upsert_query,
            (licencia, nombre_completo, row['Nombre del Club'], row['Cat. Ranking'])
        )
        # Obtenemos el ID del jugador (nuevo o existente)
        player_id = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error en UPSERT de jugador {licencia}: {e}")
        conn.rollback()
        return

    # 2. INSERT en la tabla ranking_entry
    insert_ranking_query = sql.SQL("""
        INSERT INTO ranking_entry (player_id, puntos, posicion_global, fecha_ranking)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (player_id, fecha_ranking) DO NOTHING;
    """)
    
    try:
        cursor.execute(
            insert_ranking_query,
            (player_id, row['Puntos'], row['Ranking Nacional'], fecha_ranking)
        )
        conn.commit()
    except Exception as e:
        print(f"Error al insertar ranking para {licencia}: {e}")
        conn.rollback()

# ----------------------------------------------------
# C. FUNCIÓN PRINCIPAL DE IMPORTACIÓN
# ----------------------------------------------------
def run_import(file_path: str, club_name: str, fecha_ranking: date, db_config: Dict[str, Any]):
    """Ejecuta el proceso completo de ETL (Extraer, Transformar, Cargar) y calcula el ranking interno."""
    
    conn = get_db_connection(db_config)
    if not conn:
        return
    
    print(f"Conexión a DB exitosa. Procesando archivo: {file_path}")

    # 1. Extraer y Transformar con Pandas (read_excel para XLSX)
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        conn.close()
        return

    # 2. Limpieza y Filtrado
    df[['Cat. Ranking', 'Nombre del Club']] = df[['Cat. Ranking', 'Nombre del Club']].fillna('')
    df_club = df[df['Nombre del Club'].str.upper() == club_name.upper()].copy()
    
    print(f"Encontrados {len(df_club)} jugadores para el club '{club_name}'.")

    # 3. Cargar (LOAD) - Iterar y hacer UPSERT/INSERT
    for _, row in df_club.iterrows():
        upsert_player_and_insert_ranking(conn, row, fecha_ranking)
        
    print("Datos individuales insertados. Calculando ranking interno...")

    # ----------------------------------------------------
    # 4. CÁLCULO DE POSICIÓN INTERNA DEL CLUB (SQL DML)
    # ----------------------------------------------------
    try:
        cursor = conn.cursor()
        
        # Consulta SQL para calcular y actualizar posicion_club
        calculation_query = """
            UPDATE ranking_entry AS r 
            SET posicion_club = sub.club_rank
            FROM (
                SELECT 
                    id, 
                    RANK() OVER (PARTITION BY fecha_ranking ORDER BY puntos DESC) as club_rank
                FROM ranking_entry
                -- Filtramos solo la fecha más reciente para el cálculo
                WHERE fecha_ranking = (SELECT MAX(fecha_ranking) FROM ranking_entry)
            ) AS sub
            WHERE r.id = sub.id;
        """
        cursor.execute(calculation_query)
        conn.commit() # ¡IMPORTANTE! Confirmar la transacción UPDATE
        
        print(f"Posición club actualizada para {cursor.rowcount} registros.")
        cursor.close()

    except Exception as e:
        print(f"Error al calcular la posición del club: {e}")
        conn.rollback()
    
    conn.close()
    print("Proceso de importación finalizado.")

# ----------------------------------------------------
# D. EJECUCIÓN (¡MODIFICAR ESTAS VARIABLES!)
# ----------------------------------------------------
if __name__ == "__main__":
    
    # --- CONFIGURACIÓN DE LA BASE DE DATOS ---
    DB_CONFIG = {
        'db_name': 'clubtenis_db',
        'db_user': 'postgres', 
        'db_password': 'REDACTED', # <--- ¡CONFIRMA QUE ESTA ES TU CONTRASEÑA!
        'db_host': 'localhost',
        'db_port': '5432'
    }

    # --- CONFIGURACIÓN DEL RANKING ---
    RUTA_DEL_ARCHIVO = 'ranking_M.xlsx' 
    NOMBRE_DE_TU_CLUB = 'CLUB TENIS VALGA'  
    FECHA_DEL_RANKING = date(2025, 11, 28) 

    run_import(RUTA_DEL_ARCHIVO, NOMBRE_DE_TU_CLUB, FECHA_DEL_RANKING, DB_CONFIG)