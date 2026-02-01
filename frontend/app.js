const API_URL = 'http://127.0.0.1:8000/api/ranking';   /* a esa pagina se entra para ver el json */

const rankingContainer = document.getElementById('ranking-api-container');

async function cargarRanking() {
    if (!rankingContainer) return;

    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error('Error al obtener los datos del ranking');
        }
        const jugadores = await response.json();

        const fechaActualizacion = jugadores.length > 0 ? jugadores[0].fecha_ranking : 'N/D';

        let tablaHTML = `
            <h2>Ranking del Club</h2>
            <p>Última actualización: ${fechaActualizacion}</p>
            <table>
                <thead>
                    <tr>
                        <th>Club</th>
                        <th>Global</th>
                        <th>Licencia</th>
                        <th>Nombre</th>
                        <th>Puntos</th>
                    </tr>
                </thead>
                <tbody>
        `;

        jugadores.forEach(jugador => {
            tablaHTML += `
                <tr>
                    <td>${jugador.posicion_club}</td>
                    <td>${jugador.posicion_global}</td>
                    <td>${jugador.licencia}</td>
                    <td>${jugador.nombre_completo}</td>
                    <td>${jugador.puntos}</td>
                </tr>
            `;
        });
        
        tablaHTML += `
                </tbody>
            </table>
        `;

        rankingContainer.innerHTML = tablaHTML;

    } catch (error) {
        // Manejo de errores
        console.error("Hubo un problema al cargar el ranking:", error);
        rankingContainer.innerHTML = `
            <div class="error-message">
                <h2>⚠️ Error de Conexión</h2>
                <p>No se pudo obtener el Ranking. Asegúrate de que la API está corriendo en <strong>${API_URL}</strong>.</p>
                <p>Detalles: ${error.message}</p>
            </div>
        `;
    }
}

if (rankingContainer) {
    cargarRanking(); 
} else {
    console.log("No se encontró el contenedor de ranking, la API no se cargará.");
}