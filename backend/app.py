from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from werkzeug.utils import secure_filename
import logging
import uuid
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# DeepSeek API Key from environment variable
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for file metadata
file_metadata_store = []

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx', 'xlsx', 'json', 'csv'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Helper: Check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Helper: Store file metadata
def store_file_metadata(filename, file_type, upload_time, file_id):
    metadata = {
        'file_id': file_id,
        'filename': filename,
        'file_type': file_type,
        'upload_time': upload_time,
    }
    file_metadata_store.append(metadata)
    logger.info(f"File metadata stored: {metadata}")

# API: Upload file
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        # Generate a unique file ID
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)

        # Store metadata
        upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        store_file_metadata(filename, file.filename.split('.')[-1], upload_time, file_id)

        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': filename,
            'upload_time': upload_time
        })

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# API: Chat with AI (DeepSeek)
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    file_id = data.get('file_id')

    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    # Find file metadata
    file_metadata = next((f for f in file_metadata_store if f['file_id'] == file_id), None)
    if not file_metadata:
        return jsonify({'error': 'File not found'}), 404

    # Prepare API payload for DeepSeek
    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': f'File: {file_metadata["filename"]}'},
            {'role': 'user', 'content': user_message}
        ]
    }

    try:
        # Make a request to DeepSeek API
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                'Content-Type': 'application/json',
            },
            json=payload
        )

        # Handle the response from DeepSeek
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
            return jsonify({'error': 'DeepSeek API error'}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# API: Fetch uploaded files metadata
@app.route('/api/files', methods=['GET'])
def get_files():
    return jsonify({'files': file_metadata_store})


# Home route
@app.route('/')
def home():
    return 'Hello, World!'

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)