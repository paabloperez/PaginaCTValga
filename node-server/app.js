const express = require('express');
const cors = require('cors');
const fs = require('fs/promises'); // Para gestionar tus logs de acceso
const path = require('path');

const app = express();
const PORT = 3000;

// --- 1. CONFIGURACIONES Y MIDDLEWARES ---
app.use(cors());

// Esta línea le dice a Express: "Busca los archivos en la carpeta 'public' que está al lado de este app.js"
app.use(express.static(path.join(__dirname, 'public')));

// Middleware para registrar cada visita en accesos.txt
app.use(async (req, res, next) => {
    const log = `[${new Date().toLocaleString()}] Visita a: ${req.url}\n`;
    try {
        await fs.appendFile('accesos.txt', log);
    } catch (err) {
        console.error("Error al escribir en el log:", err);
    }
    next(); // Permite que la petición siga su camino a las rutas
});

// --- 2. RUTAS DE LA API (BACKEND) ---

// Ruta para el Clima de Valga (API Externa)
app.get('/api/clima', async (req, res) => {
    try {
        const url = 'https://api.open-meteo.com/v1/forecast?latitude=42.70&longitude=-8.64&current_weather=true';
        const respuesta = await fetch(url);
        const datos = await respuesta.json();

        const temp = datos.current_weather.temperature;
        
        // Enviamos solo lo que necesitamos al frontend
        res.json({
            temp: temp,
            mensaje: temp > 15 ? "Buen tiempo para jugar al tenis 🎾" : "Hace frío, calienta bien ❄️"
        });
    } catch (error) {
        console.error("Error en API Clima:", error);
        res.status(500).json({ error: "No se pudo obtener el clima" });
    }
});

// Ruta para el Ranking (Puente con tu API de Python/Uvicorn)
app.get('/api/ranking-club', async (req, res) => {
    try {
        // Asegúrate de que tu servidor de Python esté corriendo en este puerto
        const response = await fetch('http://backend:8000/api/ranking');
        const jugadores = await response.json();
        res.json(jugadores);
    } catch (error) {
        console.error("Error en API Ranking:", error);
        res.status(500).json({ error: "No se pudo obtener el ranking desde Python" });
    }
});

// --- 3. ENCENDIDO DEL SERVIDOR ---
app.listen(PORT, () => {
    console.log('=============================================');
    console.log('🎾  SERVIDOR CLUB DE TENIS VALGA ONLINE  🎾');
    console.log(`🌐  Local:   http://localhost:${PORT}`);
    console.log(`📅  Inicio:  ${new Date().toLocaleString()}`);
    console.log('=============================================');
});