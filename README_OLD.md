# Image Caption Generator

A web application that uses AI to generate descriptive captions for uploaded images. Built with Flask backend and modern HTML/CSS/JavaScript frontend.

## Features

- **Image Upload**: Drag-and-drop or click to upload images
- **AI Captioning**: Uses BLIP (Bootstrapping Language-Image Pre-training) model for accurate image descriptions
- **Modern UI**: Clean, responsive interface with Tailwind CSS
- **Multiple Formats**: Supports PNG, JPG, JPEG, GIF, BMP, TIFF, WebP
- **Copy Caption**: One-click copy of generated captions
- **Error Handling**: Comprehensive error messages and validation

## Technology Stack

- **Backend**: Flask (Python)
- **AI Model**: Salesforce BLIP Image Captioning
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Image Processing**: Pillow (PIL)
- **Machine Learning**: PyTorch, Transformers

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project** to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd "d:\IMAGE CAPTION GENERATOR"
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Open the application in your web browser
2. Drag and drop an image onto the upload area or click to browse
3. Wait for the AI to process the image and generate a caption
4. Copy the caption or upload a new image

## File Structure

```
IMAGE CAPTION GENERATOR/
|-- app.py                 # Main Flask application
|-- requirements.txt        # Python dependencies
|-- README.md              # This file
|-- templates/
|   |-- index.html        # Frontend HTML template
|-- uploads/              # Directory for uploaded images (auto-created)
|-- static/               # Static files directory (auto-created)
```

## API Endpoints

- `GET /` - Main page with upload interface
- `POST /upload` - Upload image and generate caption
- `GET /static/uploads/<filename>` - Serve uploaded images
- `GET /health` - Health check endpoint

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- BMP
- TIFF
- WebP

## Configuration

- **Maximum file size**: 16MB
- **Host**: 0.0.0.0 (accessible from any network interface)
- **Port**: 5000

## Troubleshooting

### Common Issues

1. **Model download fails on first run**
   - The BLIP model will be downloaded automatically on first run (approximately 1.7GB)
   - Ensure you have a stable internet connection

2. **Memory errors**
   - The application requires sufficient RAM for the AI model
   - Minimum recommended: 4GB RAM

3. **Port already in use**
   - Change the port in `app.py` by modifying `port=5000` to another available port

4. **Dependencies installation fails**
   - Ensure you have Python 3.8+
   - Try upgrading pip: `python -m pip install --upgrade pip`

## Performance Notes

- First image processing may be slower due to model loading
- Subsequent processing will be faster
- GPU acceleration is not configured but could be added for better performance

## License

This project is for educational and personal use. The BLIP model is provided by Salesforce under the Apache 2.0 license.
