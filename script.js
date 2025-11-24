// script.js - VERSIÓN CON VIDEO DE EJEMPLO
const API_BASE_URL = "https://vi-nex-ai.onrender.com";

// Variable global para el video actual
let currentVideoUrl = null;
let currentJobId = null;

async function generateVideo() {
    const apiKey = document.getElementById('apiKey').value;
    const prompt = document.getElementById('prompt').value;

    if (!apiKey) {
        showStatus('Por favor ingresa tu API Key primero', 'invalid');
        return;
    }

    if (!prompt) {
        showStatus('Por favor ingresa una descripción para el video', 'invalid');
        return;
    }

    const config = document.getElementById('resolution').value;
    const style = document.getElementById('style').value;

    // Mostrar loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('generateBtn').disabled = true;
    document.getElementById('resultSection').style.display = 'block';
    document.getElementById('downloadBtn').style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('config', config);
        formData.append('style', style);

        const response = await fetch(`${API_BASE_URL}/generate-video`, {
            method: 'POST',
            headers: {
                'api-key': apiKey
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            currentJobId = data.job_id;
            showJobStatus('✅ ' + data.message);
            
            // Usar video de ejemplo (en producción sería data.video_url)
            showVideoExample();
        } else {
            throw new Error(data.detail || 'Error en el servidor');
        }

    } catch (error) {
        console.error('Error:', error);
        showJobStatus('❌ Error: ' + error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('generateBtn').disabled = false;
    }
}

// Función para mostrar video de ejemplo
function showVideoExample() {
    const videoElement = document.getElementById('generatedVideo');
    const placeholder = document.getElementById('placeholderText');
    const downloadBtn = document.getElementById('downloadBtn');
    
    placeholder.style.display = 'none';
    videoElement.style.display = 'block';
    downloadBtn.style.display = 'block';
    
    // Video de ejemplo (puedes cambiarlo por cualquier URL)
    currentVideoUrl = "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4";
    videoElement.src = currentVideoUrl;
    
    // Recargar el video para que se muestre
    videoElement.load();
    
    showJobStatus('✅ Video de ejemplo cargado - Modo simulación activo');
}

// Función de descarga REAL
function downloadVideo() {
    if (currentVideoUrl) {
        // Crear enlace de descarga
        const link = document.createElement('a');
        link.href = currentVideoUrl;
        link.download = `vi-nex-video-${currentJobId || 'demo'}.mp4`;
        link.target = '_blank';
        
        // Simular clic en el enlace
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showJobStatus('⏬ Descargando video de ejemplo...');
    } else {
        alert('No hay video disponible para descargar');
    }
}

// El resto del código se mantiene igual...
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
            showStatus('✅ API Key válida - ' + (data.mode || 'Modo producción'), 'valid');
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
    statusDiv.textContent = message;
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
