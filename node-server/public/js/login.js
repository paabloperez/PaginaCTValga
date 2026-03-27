document.getElementById('loginBtn').addEventListener('click', handleLogin);

async function handleLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('error-msg');

    // Limpiar error previo
    errorMsg.style.display = 'none';

    try {
        const response = await fetch('http://localhost:8000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            // Guardamos el token para futuras peticiones
            localStorage.setItem('adminToken', data.access_token);
            
            alert('¡Bienvenido, ' + username + '!');
            window.location.href = 'ranking.html'; 
        } else {
            errorMsg.style.display = 'block';
        }
    } catch (err) {
        console.error('Error de conexión:', err);
        alert('Error: No se pudo conectar con el servidor backend.');
    }
}