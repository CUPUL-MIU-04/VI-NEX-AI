// script.js - ACTUALIZADO para usar FormData en lugar de JSON
const API_BASE_URL = "https://vi-nex-ai.onrender.com";

async function generateVideo() {
    const apiKey = document.getElementById('apiKey').value;
    const prompt = document.getElementById('prompt').value;
    const config = document.getElementById('resolution').value;
    const style = document.getElementById('style').value;

    if (!apiKey || !prompt) {
        alert('Por favor completa todos los campos');
        return;
    }

    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = true;
    generateBtn.textContent = '⏳ Generando...';

    try {
        // Usar FormData en lugar de JSON
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('config', config);
        formData.append('style', style);

        const response = await fetch(`${API_BASE_URL}/generate-video`, {
            method: 'POST',
            headers: {
                'X-API-Key': apiKey
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showJobStatus('✅ ' + data.message);
            document.getElementById('resultSection').style.display = 'block';
        } else {
            throw new Error(data.detail || 'Error en el servidor');
        }

    } catch (error) {
        showJobStatus('❌ Error: ' + error.message);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = '🚀 Generar Video';
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
            headers: {
                'X-API-Key': apiKey
            }
        });

        if (response.ok) {
            showStatus('✅ API Key válida - Conexión exitosa', 'valid');
        } else {
            showStatus('❌ API Key inválida', 'invalid');
        }
    } catch (error) {
        showStatus('❌ Error de conexión', 'invalid');
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
