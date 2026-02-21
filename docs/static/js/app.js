const API_BASE_URL = 'https://qrgenerator-3292.onrender.com';

// DOM Elements
const form = document.getElementById('qr-form');
const urlInput = document.getElementById('url-input');
const qrResult = document.getElementById('qr-result');
const qrImage = document.getElementById('qr-image');
const urlDisplay = document.getElementById('url-display-text');
const downloadBtn = document.getElementById('download-btn');
const generateBtn = document.getElementById('generate-btn');

// Store current URL for download
let currentUrl = '';

// Generate QR Code
async function generateQR(url) {
    try {
        // Show loading state
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="btn-icon">⏳</span> Generating...';

        const response = await fetch(`${API_BASE_URL}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error('Failed to generate QR code');
        }

        const data = await response.json();

        if (data.success) {
            // Display the QR code
            qrImage.src = `data:image/png;base64,${data.qr_image}`;
            urlDisplay.textContent = data.url;
            currentUrl = data.url;
            qrResult.style.display = 'block';
            
            // Smooth scroll to result
            qrResult.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            alert('Error: ' + (data.error || 'Failed to generate QR code'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate QR code. Please check if the backend server is running.');
    } finally {
        // Reset button state
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<span class="btn-icon">⚡</span> Generate QR Code';
    }
}

// Download QR Code
async function downloadQR() {
    if (!currentUrl) {
        alert('Please generate a QR code first');
        return;
    }

    try {
        downloadBtn.disabled = true;
        downloadBtn.innerHTML = '<span class="btn-icon">⏳</span> Downloading...';

        const response = await fetch(`${API_BASE_URL}/api/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: currentUrl })
        });

        if (!response.ok) {
            throw new Error('Failed to download QR code');
        }

        // Get the blob and create download link
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = 'qr_code.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(downloadUrl);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to download QR code. Please try again.');
    } finally {
        downloadBtn.disabled = false;
        downloadBtn.innerHTML = '<span class="btn-icon">⬇️</span> Download PNG';
    }
}

// Event Listeners
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const url = urlInput.value.trim();
    if (url) {
        generateQR(url);
    }
});

downloadBtn.addEventListener('click', (e) => {
    e.preventDefault();
    downloadQR();
});

// Auto-focus input on page load
document.addEventListener('DOMContentLoaded', () => {
    urlInput.focus();
});
