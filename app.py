from flask import Flask, render_template, request, send_file, redirect, url_for, session
import qrcode
import io
import base64
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    url = ""
    
    if request.method == 'POST':
        url = request.form.get('url', '')
        if url:
            # Store URL in session and redirect
            session['url'] = url
            return redirect(url_for('index'))
    
    # Check if there's a URL in session (after redirect)
    if 'url' in session:
        url = session.pop('url')  # Get and remove from session
        # Création du QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Création de l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir l'image en base64 pour l'afficher dans le HTML
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Store the generated image in session for download
        session['qr_image'] = qr_image
        session['last_url'] = url
    
    return render_template('index.html', qr_image=qr_image, url=url)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url', '')
    if url:
        # Création du QR code
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
    
    return "No URL provided", 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
