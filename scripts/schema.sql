-- Borrar tablas si existen para evitar conflictos en reinicios limpios
DROP TABLE IF EXISTS ranking_entry;
DROP TABLE IF EXISTS players;

-- Crear tabla de Jugadores
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    licencia VARCHAR(20) UNIQUE NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    club_federacion VARCHAR(255),
    categoria VARCHAR(100)
);

-- Crear tabla de Entradas de Ranking
CREATE TABLE ranking_entry (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    puntos INTEGER,
    posicion_global INTEGER,
    posicion_club INTEGER,
    fecha_ranking DATE,
    UNIQUE(player_id, fecha_ranking)
);