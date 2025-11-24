// script.js - CON INFORMACIÓN DE MODELO
const API_BASE_URL = "https://vi-nex-ai.onrender.com";

// Variable global para el video actual
let currentVideoUrl = null;
let currentJobId = null;

// Función para verificar el estado del modelo
async function checkModelStatus() {
    const apiKey = document.getElementById('apiKey').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/model-status`, {
            headers: {
                'api-key': apiKey
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error checking model status:', error);
    }
    
    return { model_ready: false, status: 'unknown' };
}

async function generateVideo() {
    const apiKey = document.getElementById('apiKey').value;
    const prompt = document.getElementById('prompt').value;

    if (!apiKey || !prompt) {
        showStatus('Completa todos los campos', 'invalid');
        return;
    }

    // Verificar estado del modelo primero
    const modelStatus = await checkModelStatus();
    
    document.getElementById('loading').style.display = 'block';
    document.getElementById('generateBtn').disabled = true;
    document.getElementById('resultSection').style.display = 'block';

    try {
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('config', document.getElementById('resolution').value);
        formData.append('style', document.getElementById('style').value);

        const response = await fetch(`${API_BASE_URL}/generate-video`, {
            method: 'POST',
            headers: { 'api-key': apiKey },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            if (data.status === 'simulation') {
                // Mostrar información de simulación
                showSimulationResult(data, prompt);
            } else {
                // Mostrar resultado real (cuando esté disponible)
                showRealVideoResult(data);
            }
        } else {
            throw new Error(data.detail || 'Error en el servidor');
        }

    } catch (error) {
        showJobStatus('❌ Error: ' + error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('generateBtn').disabled = false;
    }
}

function showSimulationResult(data, prompt) {
    const videoElement = document.getElementById('generatedVideo');
    const placeholder = document.getElementById('placeholderText');
    const downloadBtn = document.getElementById('downloadBtn');
    
    placeholder.style.display = 'none';
    videoElement.style.display = 'block';
    downloadBtn.style.display = 'block';
    
    // Video de ejemplo
    currentVideoUrl = "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4";
    videoElement.src = currentVideoUrl;
    videoElement.load();
    
    // Mostrar información detallada
    let statusMessage = `📝 Descripción probada: "${prompt}"<br>`;
    statusMessage += `⚙️ Configuración: ${data.expected_config}<br>`;
    statusMessage += `🎨 Estilo: ${data.expected_style}<br>`;
    statusMessage += `🔧 Estado del modelo: ${data.model_status.status}<br>`;
    statusMessage += `💡 ${data.note}`;
    
    showJobStatus(statusMessage);
}

// Función de descarga
function downloadVideo() {
    if (currentVideoUrl) {
        const link = document.createElement('a');
        link.href = currentVideoUrl;
        link.download = `vi-nex-video-${currentJobId || 'demo'}.mp4`;
        link.target = '_blank';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showJobStatus('⏬ Descargando video...');
    } else {
        alert('No hay video disponible para descargar');
    }
}

// El resto de las funciones se mantienen igual...
async function testAPIKey() {
    const apiKey = document.getElementById('apiKey').value;
    const statusDiv = document.getElementById('apiStatus');
    
    if (!apiKey) {
        showStatus('Por favor ingresa tu API Key', 'invalid');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'api-key': apiKey,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            let message = '✅ API Key válida - Conexión exitosa';
            if (data.model_ready) {
                message += ' - Modelo listo para generar videos';
            } else {
                message += ' - Modelo en modo simulación';
            }
            showStatus(message, 'valid');
        } else {
            const errorData = await response.json();
            showStatus('❌ API Key inválida: ' + (errorData.detail || 'Sin permisos'), 'invalid');
        }
    } catch (error) {
        showStatus('❌ Error de conexión: ' + error.message, 'invalid');
    }
}

function showStatus(message, type) {
    const statusDiv = document.getElementById('apiStatus');
    statusDiv.textContent = message;
    statusDiv.className = `status-box status-${type}`;
}

function showJobStatus(message) {
    const statusDiv = document.getElementById('jobStatus');
    statusDiv.innerHTML = message;  // Usar innerHTML para permitir <br>
    statusDiv.style.display = 'block';
}

// Event listeners
document.getElementById('prompt').addEventListener('focus', function() {
    if (!this.value) {
        this.value = "Un paisaje montañoso al atardecer con nubes coloridas";
    }
});

let apiKeyTimeout;
document.getElementById('apiKey').addEventListener('input', function() {
    clearTimeout(apiKeyTimeout);
    if (this.value.length >= 10) {
        apiKeyTimeout = setTimeout(testAPIKey, 1000);
    }
});

// Inicializar el video element
document.addEventListener('DOMContentLoaded', function() {
    const videoElement = document.getElementById('generatedVideo');
    videoElement.controls = true;
});

console.log('🎬 VI-NEX-AI Frontend loaded - Modo Simulación');
