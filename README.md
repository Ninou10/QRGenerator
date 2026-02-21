# QrGenerator

A simple and elegant QR Code Generator web application with separate frontend and backend for easy deployment.

## Features

-  Instant QR code generation
-  Download QR codes as PNG
-  Modern dark theme UI
-  Animated background effects

## Project Structure

```
├── app.py              # Flask API backend (deploy to Render)
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── docs/               # Frontend (deploy to GitHub Pages)
│   ├── index.html
│   └── static/
│       ├── logo.png
│       └── js/app.js
└── static/             # Backend static files
```

## Deployment

### Backend (Render)

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml` and configure:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Click "Create Web Service"
7. Note your Render URL (e.g., `https://your-app.onrender.com`)

### Frontend (GitHub Pages)

1. **Update API URL**: Edit `docs/static/js/app.js` and set your Render URL:
   ```javascript
   const API_BASE_URL = 'https://your-app.onrender.com';
   ```

2. Go to your GitHub repository → Settings → Pages
3. Under "Source", select:
   - Branch: `main`
   - Folder: `/docs`
4. Click Save
5. Your frontend will be live at `https://yourusername.github.io/reponame`

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/Ninou10/QRGenerator.git
cd QRGenerator
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend:
```bash
python app.py
```

5. For local testing, update `docs/static/js/app.js`:
```javascript
const API_BASE_URL = 'http://127.0.0.1:5000';
```

6. Open `docs/index.html` in your browser

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate` | Generate QR code (returns base64 image) |
| POST | `/api/download` | Download QR code as PNG file |
| GET | `/health` | Health check endpoint |

### Example Request

```bash
curl -X POST https://your-app.onrender.com/api/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Technologies

- **Backend**: Python 3, Flask, Flask-CORS, qrcode, Pillow, Gunicorn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## Author

Made by [Ninou10](https://github.com/Ninou10)

## License

MIT License
