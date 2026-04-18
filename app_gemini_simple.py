from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import uuid

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure Gemini API - you can set this directly or via environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or "YOUR_GEMINI_API_KEY_HERE"

# Initialize Gemini model only when API key is provided
model = None
if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Gemini 2.5 Flash API configured successfully")
    except Exception as e:
        print(f"❌ Error configuring Gemini API: {e}")
        model = None
else:
    print("⚠️  Gemini API key not configured")

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_caption(image_path):
    """Generate caption using Gemini AI"""
    try:
        if model is None:
            return "Gemini API not configured. Please set your API key."
        
        # Open and prepare image
        image = Image.open(image_path)
        
        # Generate caption with Gemini
        response = model.generate_content([
            "Generate exactly 5 social media captions for this image. Each caption should be Instagram-worthy (maximum 25 words). Include variety: one poetic, one funny, one inspirational, one descriptive, and one trendy. Format: 1. [poetic caption] 2. [funny caption] 3. [inspirational caption] 4. [descriptive caption] 5. [trendy caption]. No extra text.",
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
    api_configured = model is not None
    return jsonify({
        'status': 'healthy', 
        'model': 'gemini-2.5-flash',
        'api_configured': api_configured
    })

if __name__ == '__main__':
    print("Starting Image Caption Generator with Gemini AI...")
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("⚠️  WARNING: Gemini API key not configured!")
        print("Set your API key in GEMINI_API_KEY environment variable")
        print("Or edit this file and replace YOUR_GEMINI_API_KEY_HERE")
    app.run(debug=True, host='127.0.0.1', port=5000)
