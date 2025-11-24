/**
 * API Client para Sistema de Visitas con JWT
 * ES03 - Programación Backend
 */

const API_URL = localStorage.getItem('API_URL') || 'http://127.0.0.1:8000';

/**
 * Obtiene el token de acceso
 */
function getAccessToken() {
    return localStorage.getItem('access_token');
}

/**
 * Obtiene el token de refresh
 */
function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

/**
 * Verifica si el usuario está autenticado
 */
function isAuthenticated() {
    return !!getAccessToken();
}

/**
 * Refresca el token de acceso
 */
async function refreshToken() {
    const refresh = getRefreshToken();
    
    if (!refresh) {
        logout();
        return null;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/token/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return data.access;
        } else {
            logout();
            return null;
        }
    } catch (error) {
        console.error('Error refreshing token:', error);
        logout();
        return null;
    }
}

/**
 * Realiza una petición HTTP autenticada
 */
async function authenticatedFetch(url, options = {}) {
    let token = getAccessToken();
    
    if (!token) {
        window.location.href = 'login.html';
        return null;
    }
    
    // Agregar headers de autenticación
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
    };
    
    try {
        let response = await fetch(url, options);
        
        // Si el token expiró, intentar refrescarlo
        if (response.status === 401) {
            token = await refreshToken();
            
            if (token) {
                options.headers['Authorization'] = `Bearer ${token}`;
                response = await fetch(url, options);
            } else {
                window.location.href = 'login.html';
                return null;
            }
        }
        
        return response;
    } catch (error) {
        console.error('Error en petición:', error);
        throw error;
    }
}

/**
 * Cierra la sesión
 */
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    window.location.href = 'login.html';
}

/**
 * API Methods - Visitas
 */

// Obtener todas las visitas
async function getVisitas(page = 1) {
    const response = await authenticatedFetch(`${API_URL}/api/visitas/?page=${page}`);
    if (response && response.ok) {
        return await response.json();
    }
    return null;
}

// Obtener una visita específica
async function getVisita(id) {
    const response = await authenticatedFetch(`${API_URL}/api/visitas/${id}/`);
    if (response && response.ok) {
        return await response.json();
    }
    return null;
}

// Crear una visita
async function createVisita(data) {
    const response = await authenticatedFetch(`${API_URL}/api/visitas/`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    
    if (response && response.ok) {
        return await response.json();
    } else if (response) {
        const error = await response.json();
        throw new Error(JSON.stringify(error));
    }
    return null;
}

// Actualizar una visita
async function updateVisita(id, data) {
    const response = await authenticatedFetch(`${API_URL}/api/visitas/${id}/`, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
    
    if (response && response.ok) {
        return await response.json();
    } else if (response) {
        const error = await response.json();
        throw new Error(JSON.stringify(error));
    }
    return null;
}

// Actualización parcial de una visita
async function patchVisita(id, data) {
    const response = await authenticatedFetch(`${API_URL}/api/visitas/${id}/`, {
        method: 'PATCH',
        body: JSON.stringify(data)
    });
    
    if (response && response.ok) {
        return await response.json();
    } else if (response) {
        const error = await response.json();
        throw new Error(JSON.stringify(error));
    }
    return null;
}

// Eliminar una visita
async function deleteVisita(id) {
    const response = await authenticatedFetch(`${API_URL}/api/visitas/${id}/`, {
        method: 'DELETE'
    });
    
    return response && (response.ok || response.status === 204);
}

// Obtener visitas activas
async function getVisitasActivas() {
    const response = await authenticatedFetch(`${API_URL}/api/visitas/activas/`);
    if (response && response.ok) {
        return await response.json();
    }
    return null;
}

// Obtener visitas completadas
async function getVisitasCompletadas() {
    const response = await authenticatedFetch(`${API_URL}/api/visitas/completadas/`);
    if (response && response.ok) {
        return await response.json();
    }
    return null;
}

// Marcar salida de una visita
async function marcarSalida(id) {
    const response = await authenticatedFetch(`${API_URL}/api/visitas/${id}/marcar_salida/`, {
        method: 'POST'
    });
    
    if (response && response.ok) {
        return await response.json();
    } else if (response) {
        const error = await response.json();
        throw new Error(JSON.stringify(error));
    }
    return null;
}

/**
 * Utilities
 */

// Formatear fecha
function formatearFecha(fecha) {
    const date = new Date(fecha);
    return date.toLocaleString('es-CL', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Mostrar alerta
function showAlert(type, message) {
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const icon = type === 'success' ? 'bi-check-circle' : 'bi-x-circle';
    
    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        alertContainer.innerHTML = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                <i class="bi ${icon}"></i> ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                alert.classList.remove('show');
                setTimeout(() => alert.remove(), 150);
            }
        }, 5000);
    }
}
