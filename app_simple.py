from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from PIL import Image
import uuid
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_caption(image_path):
    """Generate a mock caption based on image analysis"""
    try:
        # Basic image analysis
        img = Image.open(image_path)
        width, height = img.size
        aspect_ratio = width / height
        
        # Mock caption generation based on image properties
        captions = [
            f"A beautiful image with dimensions {width}x{height} pixels",
            f"A stunning photograph captured in high resolution",
            "An interesting visual composition with vibrant colors",
            "A well-composed image showing artistic expression",
            "A captivating scene with excellent lighting",
            f"A rectangular image with aspect ratio {aspect_ratio:.2f}",
            "A visually appealing photograph with good composition",
            "An artistic image showcasing creative photography",
            "A detailed image with rich textures and patterns",
            "A professional-quality photograph with great clarity"
        ]
        
        # Add some variety based on image size
        if width > 1000 or height > 1000:
            captions.extend([
                "A high-resolution image suitable for large displays",
                "A detailed photograph perfect for close examination",
                "A professional-grade image with excellent detail"
            ])
        elif width < 500 and height < 500:
            captions.extend([
                "A compact image optimized for web use",
                "A smaller image with efficient file size",
                "A web-friendly photograph with good quality"
            ])
        
        return random.choice(captions)
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

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
    return jsonify({'status': 'healthy', 'model': 'mock_caption_generator'})

if __name__ == '__main__':
    print("Starting Image Caption Generator (Simple Version)...")
    print("This version uses mock captions for demonstration purposes.")
    app.run(debug=True, host='0.0.0.0', port=5000)
