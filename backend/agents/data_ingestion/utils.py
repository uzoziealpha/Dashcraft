import os

# Validate file extension
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Create unique file names
def generate_unique_filename(filename):
    return str(uuid.uuid4()) + "_" + secure_filename(filename)