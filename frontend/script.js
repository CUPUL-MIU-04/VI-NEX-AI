// Configuración - CAMBIA ESTA URL por tu API desplegada
const API_BASE_URL = "https://tu-api-vi-nex-ai.herokuapp.com"; // o tu dominio

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
        showStatus('❌ Error de conexión: ' + error.message, 'invalid');
    }
}

async function generateVideo() {
    const apiKey = document.getElementById('apiKey').value;
    const prompt = document.getElementById('prompt').value;
    const resolution = document.getElementById('resolution').value;

    if (!apiKey || !prompt) {
        alert('Por favor completa todos los campos');
        return;
    }

    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = true;
    generateBtn.textContent = '⏳ Generando...';

    try {
        const response = await fetch(`${API_BASE_URL}/generate-video`, {
            method: 'POST',
            headers: {
                'X-API-Key': apiKey,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                config: resolution
            })
        });

        const data = await response.json();

        if (response.ok) {
            showResult('✅ Video en proceso. ID: ' + data.job_id);
        } else {
            throw new Error(data.detail || 'Error desconocido');
        }
    } catch (error) {
        showResult('❌ Error: ' + error.message);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = '🚀 Generar Video';
    }
}

function showStatus(message, type) {
    const statusDiv = document.getElementById('apiStatus');
    statusDiv.textContent = message;
    statusDiv.className = `status-${type}`;
    statusDiv.style.display = 'block';
}

function showResult(message) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `<div class="status-valid">${message}</div>`;
          }
