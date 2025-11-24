// script.js - HEADER CORREGIDO
const API_BASE_URL = "https://vi-nex-ai.onrender.com";

// Función para probar API Key - CORREGIDA
async function testAPIKey() {
    const apiKey = document.getElementById('apiKey').value;
    const statusDiv = document.getElementById('apiStatus');
    
    if (!apiKey) {
        showStatus('Por favor ingresa tu API Key', 'invalid');
        return;
    }

    try {
        console.log('🔑 Enviando API Key:', apiKey);
        
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'api-key': apiKey,  // ← CAMBIADO: 'api-key' en lugar de 'X-API-Key'
                'Content-Type': 'application/json'
            }
        });

        console.log('📡 Respuesta del servidor:', response.status);

        if (response.ok) {
            const data = await response.json();
            showStatus('✅ API Key válida - Conexión exitosa', 'valid');
            return true;
        } else {
            const errorData = await response.json();
            showStatus('❌ API Key inválida: ' + (errorData.detail || 'Sin permisos'), 'invalid');
            return false;
        }
    } catch (error) {
        console.error('💥 Error de conexión:', error);
        showStatus('❌ Error de conexión: ' + error.message, 'invalid');
        return false;
    }
}

// Función para generar video - CORREGIDA
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

    try {
        // Usar FormData como espera el backend
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('config', config);
        formData.append('style', style);

        console.log('🚀 Enviando solicitud de video...');
        
        const response = await fetch(`${API_BASE_URL}/generate-video`, {
            method: 'POST',
            headers: {
                'api-key': apiKey  // ← CAMBIADO: 'api-key' en lugar de 'X-API-Key'
                // NO incluir 'Content-Type' cuando usas FormData
            },
            body: formData
        });

        console.log('📡 Respuesta de generación:', response.status);

        const data = await response.json();

        if (response.ok) {
            showJobStatus('✅ ' + data.message);
            // Simular video generado
            simulateVideoResult();
        } else {
            throw new Error(data.detail || 'Error en el servidor');
        }

    } catch (error) {
        console.error('💥 Error:', error);
        showJobStatus('❌ Error: ' + error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('generateBtn').disabled = false;
    }
}

// Funciones utilitarias (mantener igual)
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

function simulateVideoResult() {
    setTimeout(() => {
        const videoElement = document.getElementById('generatedVideo');
        const placeholder = document.getElementById('placeholderText');
        const downloadBtn = document.getElementById('downloadBtn');
        
        placeholder.style.display = 'none';
        videoElement.style.display = 'block';
        downloadBtn.style.display = 'block';
        
        showJobStatus('✅ Video generado exitosamente - Esta es una simulación');
    }, 3000);
}

function downloadVideo() {
    alert('En una implementación real, aquí se descargaría el video generado');
}

// Event listeners
document.getElementById('prompt').addEventListener('focus', function() {
    if (!this.value) {
        this.value = "Un paisaje montañoso al atardecer con nubes coloridas";
    }
});

// Verificar API Key automáticamente
let apiKeyTimeout;
document.getElementById('apiKey').addEventListener('input', function() {
    clearTimeout(apiKeyTimeout);
    if (this.value.length >= 10) {
        apiKeyTimeout = setTimeout(testAPIKey, 1000);
    }
});

console.log('🎬 VI-NEX-AI Frontend loaded - API URL:', API_BASE_URL);
