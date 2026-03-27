document.addEventListener('DOMContentLoaded', () => {
    // --- PARTE A: GESTIÓN DE USUARIO (SALUDO) ---
    const token = localStorage.getItem('adminToken');
    const welcomeMsg = document.getElementById('welcome-msg');
    const authBtn = document.getElementById('auth-btn');

    if (token) {
        try {
            // Decodificamos el nombre del admin desde el Token JWT
            const payload = JSON.parse(atob(token.split('.')[1]));
            welcomeMsg.innerHTML = `👋 Hola, <strong>${payload.sub}</strong>`;
            
            authBtn.textContent = 'Cerrar Sesión';
            authBtn.classList.add('logout');
            authBtn.onclick = () => {
                localStorage.removeItem('adminToken');
                window.location.reload();
            };
        } catch (e) {
            localStorage.removeItem('adminToken');
        }
    } else {
        authBtn.onclick = () => { window.location.href = 'login.html'; };
    }

    // --- PARTE B: CARGAR DATOS DEL RANKING ---
    cargarRanking();
});

async function cargarRanking() {
    try {
        const response = await fetch('http://localhost:8000/api/ranking');
        const datos = await response.json();
        
        const tabla = document.querySelector('#tabla-ranking tbody'); // Ajusta el ID a tu tabla
        tabla.innerHTML = ""; // Limpiar tabla

        datos.forEach((jugador, index) => {
            const fila = `
                <tr>
                    <td>${index + 1}</td>
                    <td>${jugador.nombre_completo}</td>
                    <td>${jugador.puntos}</td>
                    <td>${jugador.categoria}</td>
                </tr>
            `;
            tabla.innerHTML += fila;
        });
    } catch (error) {
        console.error("Error cargando ranking:", error);
    }
}