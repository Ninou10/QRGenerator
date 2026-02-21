from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import qrcode
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/generate', methods=['POST'])
def generate_qr():
    """Generate QR code and return as base64"""
    data = request.get_json()
    url = data.get('url', '') if data else ''
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return jsonify({
        'success': True,
        'qr_image': qr_image,
        'url': url
    })

@app.route('/api/download', methods=['POST'])
def download():
    """Download QR code as PNG file"""
    data = request.get_json()
    url = data.get('url', '') if data else ''
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='qr_code.png')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
