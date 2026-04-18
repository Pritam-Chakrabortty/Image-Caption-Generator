from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import google.generativeai as genai
from PIL import Image
import uuid
import base64
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_caption(image_path):
    """Generate caption using Gemini AI"""
    try:
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            return "Please set your Gemini API key in the GEMINI_API_KEY environment variable"
        
        # Open and prepare image
        image = Image.open(image_path)
        
        # Generate caption with Gemini
        response = model.generate_content([
            "Generate a descriptive caption for this image. Be detailed and specific about what you see.",
            image
        ])
        
        return response.text.strip()
        
    except Exception as e:
        return f"Error generating caption: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Generate caption
        caption = generate_caption(filepath)
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'caption': caption,
            'image_url': f'/static/uploads/{unique_filename}'
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/health')
def health_check():
    api_configured = GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE"
    return jsonify({
        'status': 'healthy', 
        'model': 'gemini-1.5-flash',
        'api_configured': api_configured
    })

if __name__ == '__main__':
    print("Starting Image Caption Generator with Gemini AI...")
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("⚠️  WARNING: Gemini API key not configured!")
        print("Please set your Gemini API key in the GEMINI_API_KEY environment variable")
    else:
        print("✅ Gemini API key configured successfully")
    app.run(debug=True, host='0.0.0.0', port=5000)
