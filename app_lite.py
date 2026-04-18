from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load a smaller model for faster startup
try:
    processor = AutoProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    model = AutoModelForVision2Seq.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    # Fallback to a very basic caption if model fails
    processor = None
    model = None

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_caption(image_path):
    try:
        if model is None or processor is None:
            return "AI model not available. Please check server logs."
        
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt")
        pixel_values = inputs.pixel_values
        
        # Generate caption
        generated_ids = model.generate(pixel_values, max_length=50)
        caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return caption
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
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    print("Starting Image Caption Generator...")
    print("Please wait for the model to load...")
    app.run(debug=True, host='0.0.0.0', port=5000)
