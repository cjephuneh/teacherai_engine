# app.py
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import pdfplumber
import openai
from flask_cors import CORS


# Initialize Flask app
app = Flask(__name__)

CORS(app, origins="http://localhost:3000")  # This allows CORS for all routes from localhost:3000

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# OpenAI Client setup
openai.api_key = OPENAI_API_KEY

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text

def generate_questions(text):
    # Replace this with the actual implementation of calling GPT-4 to generate questions
    response = openai.Completion.create(
    engine="text-davinci-003",  # Updated model name for GPT-3
    prompt="Create some questions based on the following text: {}".format(text),
    n=5,
    max_tokens=1024
)
    return response.choices[0].text.strip()

# Routes
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Extract text from PDF
        text = extract_text_from_pdf(file_path)
        
        # Generate questions using GPT-4
        questions = generate_questions(text)
        
        # Save questions to file (or database) and generate a link (implement this functionality)
        # For now, just return the questions as a response
        return jsonify({'questions': questions}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/quiz/<quiz_id>')
def get_quiz(quiz_id):
    # Load the quizzes from a JSON file or database
    with open('quizzes.json', 'r') as f:
        quizzes = json.load(f)
    
    # Find the quiz by the unique identifier
    quiz = quizzes.get(quiz_id)
    if quiz is not available:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Send the quiz to the frontend
    return jsonify(quiz), 200



if __name__ == '__main__':
    app.run(debug=True)
