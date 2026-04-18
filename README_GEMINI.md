# Image Caption Generator with Gemini AI

A web application that uses Google's Gemini AI to generate descriptive captions for uploaded images. This version provides real AI-powered image analysis.

## Features

- **Real AI Captioning**: Uses Google's Gemini 1.5 Flash model for accurate image descriptions
- **Image Upload**: Drag-and-drop or click to upload images
- **Modern UI**: Clean, responsive interface with Tailwind CSS
- **Multiple Formats**: Supports PNG, JPG, JPEG, GIF, BMP, TIFF, WebP
- **API Key Security**: Secure API key configuration
- **Error Handling**: Comprehensive error messages and validation

## Technology Stack

- **Backend**: Flask (Python)
- **AI Model**: Google Gemini 1.5 Flash
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Image Processing**: Pillow (PIL)
- **AI Integration**: Google Generative AI

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Step 1: Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 2: Configure API Key

**Option A: Environment Variable (Recommended)**
```bash
# Windows
set GEMINI_API_KEY=your_actual_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_actual_api_key_here
```

**Option B: Edit the Application**
1. Open `app_gemini_simple.py`
2. Replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app_gemini_simple.py
```

### Step 5: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Open the application in your web browser
2. Drag and drop an image onto the upload area or click to browse
3. Wait for Gemini AI to analyze the image and generate a caption
4. Copy the caption or upload a new image

## API Configuration

The application supports multiple configuration methods:

### Environment Variables
- `GEMINI_API_KEY`: Your Gemini API key

### Health Check
The `/health` endpoint provides status information:
```json
{
  "status": "healthy",
  "model": "gemini-1.5-flash",
  "api_configured": true
}
```

## File Structure

```
IMAGE CAPTION GENERATOR/
|-- app_gemini_simple.py   # Main application with Gemini integration
|-- requirements.txt       # Python dependencies
|-- .env.example          # Environment variable template
|-- setup_gemini.py       # Setup script
|-- templates/
|   |-- index.html       # Frontend HTML template
|-- uploads/             # Directory for uploaded images
```

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- BMP
- TIFF
- WebP

## API Limits and Pricing

- Gemini API offers a generous free tier
- Check [Google AI Pricing](https://ai.google.dev/pricing) for current limits
- Free tier typically includes:
  - 15 requests per minute
  - 1,500 requests per day

## Troubleshooting

### Common Issues

1. **"Gemini API not configured" error**
   - Ensure your API key is set correctly
   - Check that the API key has proper permissions

2. **API rate limit exceeded**
   - Wait a few minutes and try again
   - Consider upgrading to a paid plan for higher limits

3. **Invalid API key**
   - Verify your API key is correct
   - Ensure it's not expired

4. **Network connectivity issues**
   - Check your internet connection
   - Verify firewall settings allow API access

### Debug Mode

The application runs in debug mode by default. Check the console output for detailed error messages.

## Security Notes

- Never commit your API key to version control
- Use environment variables in production
- The application runs on localhost by default for security

## Advanced Configuration

### Custom Prompt

You can modify the caption generation prompt in the `generate_caption()` function:

```python
response = model.generate_content([
    "Generate a detailed caption for this image focusing on objects, colors, and composition.",
    image
])
```

### Model Selection

Change the model by modifying the model initialization:

```python
model = genai.GenerativeModel('gemini-1.5-pro')  # More powerful model
```

## License

This project is for educational and personal use. The Gemini API usage is subject to Google's terms of service.
