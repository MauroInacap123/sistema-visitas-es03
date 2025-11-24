/**
 * Dashboard Logic - Sistema de Visitas
 * ES03 - Programación Backend
 */

let visitaModal;
let deleteModal;
let visitaIdToDelete = null;
let currentPage = 1;

// Al cargar la página
document.addEventListener('DOMContentLoaded', async () => {
    // Verificar autenticación
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }
    
    // Mostrar nombre de usuario
    const username = localStorage.getItem('username');
    document.getElementById('username').textContent = username;
    
    // Inicializar modales
    visitaModal = new bootstrap.Modal(document.getElementById('visitaModal'));
    deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    
    // Cargar datos
    await cargarDatos();
});

/**
 * Carga todos los datos del dashboard
 */
async function cargarDatos(page = 1) {
    currentPage = page;
    await Promise.all([
        cargarEstadisticas(),
        cargarVisitas(page)
    ]);
}

/**
 * Carga las estadísticas
 */
async function cargarEstadisticas() {
    try {
        const [activas, completadas] = await Promise.all([
            getVisitasActivas(),
            getVisitasCompletadas()
        ]);
        
        const totalActivas = activas ? activas.length : 0;
        const totalCompletadas = completadas ? completadas.length : 0;
        const total = totalActivas + totalCompletadas;
        
        document.getElementById('totalVisitas').textContent = total;
        document.getElementById('visitasActivas').textContent = totalActivas;
        document.getElementById('visitasCompletadas').textContent = totalCompletadas;
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
    }
}

/**
 * Carga la lista de visitas
 */
async function cargarVisitas(page = 1) {
    try {
        const data = await getVisitas(page);
        
        if (!data) {
            document.getElementById('visitasTable').innerHTML = `
                <tr><td colspan="8" class="text-center text-danger">Error al cargar visitas</td></tr>
            `;
            return;
        }
        
        const tbody = document.getElementById('visitasTable');
        
        if (data.results && data.results.length > 0) {
            tbody.innerHTML = data.results.map(visita => `
                <tr>
                    <td>${visita.id}</td>
                    <td>${visita.rut}</td>
                    <td>${visita.nombre}</td>
                    <td>${visita.motivo.substring(0, 30)}${visita.motivo.length > 30 ? '...' : ''}</td>
                    <td>${formatearFecha(visita.fecha_entrada)}</td>
                    <td>${visita.hora_salida || '-'}</td>
                    <td>
                        <span class="badge ${visita.hora_salida ? 'bg-secondary' : 'bg-success'}">
                            ${visita.hora_salida ? 'Completado' : 'Activo'}
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="verVisita(${visita.id})" title="Ver">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-warning" onclick="editarVisita(${visita.id})" title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="eliminarVisita(${visita.id}, '${visita.nombre}')" title="Eliminar">
                            <i class="bi bi-trash"></i>
                        </button>
                        ${!visita.hora_salida ? `
                        <button class="btn btn-sm btn-success" onclick="marcarSalidaVisita(${visita.id})" title="Marcar Salida">
                            <i class="bi bi-check-circle"></i>
                        </button>
                        ` : ''}
                    </td>
                </tr>
            `).join('');
            
            // Generar paginación
            generarPaginacion(data);
        } else {
            tbody.innerHTML = `
                <tr><td colspan="8" class="text-center">No hay visitas registradas</td></tr>
            `;
        }
    } catch (error) {
        console.error('Error cargando visitas:', error);
        showAlert('error', 'Error al cargar las visitas');
    }
}

/**
 * Genera la paginación
 */
function generarPaginacion(data) {
    const pagination = document.getElementById('pagination');
    
    if (!data.next && !data.previous) {
        pagination.innerHTML = '';
        return;
    }
    
    let html = '';
    
    // Botón anterior
    if (data.previous) {
        html += `<li class="page-item"><a class="page-link" href="#" onclick="cargarDatos(${currentPage - 1})">Anterior</a></li>`;
    }
    
    // Página actual
    html += `<li class="page-item active"><span class="page-link">${currentPage}</span></li>`;
    
    // Botón siguiente
    if (data.next) {
        html += `<li class="page-item"><a class="page-link" href="#" onclick="cargarDatos(${currentPage + 1})">Siguiente</a></li>`;
    }
    
    pagination.innerHTML = html;
}

/**
 * Prepara el formulario para nueva visita
 */
function nuevoFormulario() {
    document.getElementById('modalTitle').textContent = 'Nueva Visita';
    document.getElementById('visitaForm').reset();
    document.getElementById('visitaId').value = '';
    document.getElementById('horaSalidaGroup').style.display = 'none';
}

/**
 * Ver detalles de una visita
 */
async function verVisita(id) {
    try {
        const visita = await getVisita(id);
        
        if (visita) {
            alert(`
                ID: ${visita.id}
                RUT: ${visita.rut}
                Nombre: ${visita.nombre}
                Motivo: ${visita.motivo}
                Entrada: ${formatearFecha(visita.fecha_entrada)}
                Salida: ${visita.hora_salida || 'No registrada'}
            `);
        }
    } catch (error) {
        showAlert('error', 'Error al obtener la visita');
    }
}

/**
 * Editar una visita
 */
async function editarVisita(id) {
    try {
        const visita = await getVisita(id);
        
        if (visita) {
            document.getElementById('modalTitle').textContent = 'Editar Visita';
            document.getElementById('visitaId').value = visita.id;
            document.getElementById('rut').value = visita.rut;
            document.getElementById('nombre').value = visita.nombre;
            document.getElementById('motivo').value = visita.motivo;
            
            if (visita.hora_salida) {
                document.getElementById('horaSalidaGroup').style.display = 'block';
                document.getElementById('hora_salida').value = visita.hora_salida;
            }
            
            visitaModal.show();
        }
    } catch (error) {
        showAlert('error', 'Error al cargar la visita');
    }
}

/**
 * Guarda una visita (crear o actualizar)
 */
async function guardarVisita() {
    const id = document.getElementById('visitaId').value;
    const data = {
        rut: document.getElementById('rut').value,
        nombre: document.getElementById('nombre').value,
        motivo: document.getElementById('motivo').value,
    };
    
    // Si estamos editando y hay hora de salida
    if (id && document.getElementById('hora_salida').value) {
        data.hora_salida = document.getElementById('hora_salida').value;
    }
    
    try {
        if (id) {
            // Actualizar
            await updateVisita(id, data);
            showAlert('success', 'Visita actualizada exitosamente');
        } else {
            // Crear
            await createVisita(data);
            showAlert('success', 'Visita creada exitosamente');
        }
        
        visitaModal.hide();
        await cargarDatos(currentPage);
    } catch (error) {
        const errorMsg = JSON.parse(error.message);
        let errorText = 'Error al guardar la visita';
        
        if (errorMsg.rut) {
            errorText = errorMsg.rut[0];
        }
        
        showAlert('error', errorText);
    }
}

/**
 * Prepara la eliminación de una visita
 */
function eliminarVisita(id, nombre) {
    visitaIdToDelete = id;
    document.getElementById('deleteVisitaInfo').textContent = nombre;
    deleteModal.show();
}

/**
 * Confirma la eliminación
 */
async function confirmarEliminar() {
    if (!visitaIdToDelete) return;
    
    try {
        const success = await deleteVisita(visitaIdToDelete);
        
        if (success) {
            showAlert('success', 'Visita eliminada exitosamente');
            deleteModal.hide();
            await cargarDatos(currentPage);
        } else {
            showAlert('error', 'Error al eliminar la visita');
        }
    } catch (error) {
        showAlert('error', 'Error al eliminar la visita');
    }
    
    visitaIdToDelete = null;
}

/**
 * Marca la salida de una visita
 */
async function marcarSalidaVisita(id) {
    try {
        await marcarSalida(id);
        showAlert('success', 'Salida registrada exitosamente');
        await cargarDatos(currentPage);
    } catch (error) {
        const errorMsg = JSON.parse(error.message);
        showAlert('error', errorMsg.error || 'Error al marcar salida');
    }
}
