// ================= CONFIGURACIÓN =================
// IMPORTANTE: Cambia esta URL por tu API real cuando la despliegues
const API_BASE_URL = "https://tu-api-vi-nex-ai.herokuapp.com";

// Variables globales
let currentJobId = null;
let currentVideoUrl = null;

// ================= FUNCIONES PRINCIPALES =================

// Probar la API Key
async function testAPIKey() {
    const apiKey = document.getElementById('apiKey').value;
    const statusDiv = document.getElementById('apiStatus');
    
    if (!apiKey) {
        showStatus('Por favor ingresa tu API Key', 'invalid');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            headers: {
                'X-API-Key': apiKey
            }
        });

        if (response.ok) {
            showStatus('✅ API Key válida - Conexión exitosa con VI-NEX-AI', 'valid');
        } else {
            showStatus('❌ API Key inválida o sin permisos', 'invalid');
        }
    } catch (error) {
        showStatus('❌ Error de conexión: Verifica que la API esté activa', 'invalid');
        console.error('Error:', error);
    }
}

// Generar video
async function generateVideo() {
    const apiKey = document.getElementById('apiKey').value;
    const prompt = document.getElementById('prompt').value;

    if (!apiKey) {
        showStatus('Por favor ingresa y verifica tu API Key primero', 'invalid');
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

    try {
        const response = await fetch(`${API_BASE_URL}/generate-video`, {
            method: 'POST',
            headers: {
                'X-API-Key': apiKey,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                config: config,
                style: style
            })
        });

        const data = await response.json();

        if (response.ok) {
            currentJobId = data.job_id;
            showJobStatus('✅ Video en proceso. ID: ' + data.job_id);
            
            // Simular progreso (en producción harías polling real)
            simulateProgress();
        } else {
            throw new Error(data.detail || 'Error en el servidor');
        }

    } catch (error) {
        showJobStatus('❌ Error: ' + error.message);
        document.getElementById('loading').style.display = 'none';
        document.getElementById('generateBtn').disabled = false;
    }
}

// Simular progreso de generación
function simulateProgress() {
    setTimeout(() => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('generateBtn').disabled = false;
        
        // Mostrar video de ejemplo (en producción sería el video real de tu API)
        const videoElement = document.getElementById('generatedVideo');
        const placeholder = document.getElementById('placeholderText');
        const downloadBtn = document.getElementById('downloadBtn');
        
        placeholder.style.display = 'none';
        videoElement.style.display = 'block';
        downloadBtn.style.display = 'block';
        
        // En producción, usarías la URL real del video generado
        // videoElement.src = `${API_BASE_URL}/videos/${currentJobId}.mp4`;
        // currentVideoUrl = videoElement.src;
        
        showJobStatus('✅ Video generado exitosamente');
        
    }, 8000); // Simular 8 segundos de procesamiento
}

// Descargar video
function downloadVideo() {
    if (currentVideoUrl) {
        const link = document.createElement('a');
        link.href = currentVideoUrl;
        link.download = `vi-nex-video-${currentJobId}.mp4`;
        link.click();
    } else {
        alert('Video no disponible para descargar');
    }
}

// ================= FUNCIONES UTILITARIAS =================

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

// ================= EVENT LISTENERS =================

// Cargar ejemplo de prompt al hacer focus
document.getElementById('prompt').addEventListener('focus', function() {
    if (!this.value) {
        this.value = "Un paisaje montañoso al atardecer con nubes coloridas y un río cristalino fluyendo en primer plano, estilo cinematográfico";
    }
});

// Generar con Enter en el textarea
document.getElementById('prompt').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        generateVideo();
    }
});

// Verificar API Key automáticamente al escribir
let apiKeyTimeout;
document.getElementById('apiKey').addEventListener('input', function() {
    clearTimeout(apiKeyTimeout);
    if (this.value.length > 10) {
        apiKeyTimeout = setTimeout(testAPIKey, 1000);
    }
});

// ================= INICIALIZACIÓN =================
console.log('VI-NEX-AI Frontend loaded successfully');
console.log('API Base URL:', API_BASE_URL);
