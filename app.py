from flask import Flask, request, jsonify, send_file, abort
import requests
import json
import openai
import os
import io
from flask import session
from pdfminer.high_level import extract_text_to_fp
from io import BytesIO

# Set up Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Set up folder for file uploads
app.config['tmp'] = './tmp'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

@app.route('/')
def index():
    return send_file('index.html')

# Set up OpenAI API key
openai.api_key = "YOUR_API_KEY"

questions = []
correct_answers = {}  # Initialize the dictionary to store correct answers

# Route for generating quiz questions
@app.route('/quiz-generator', methods=['POST']) 
def generate_quiz():
    # Check if the file was submitted
    if 'file' not in request.files:
        abort(400, description='No file was submitted.')
        
    # Get the PDF file and read the text
    file = request.files['file']
    # Check if the file is a PDF
    if not file.filename.lower().endswith('.pdf'):
        abort(400, description='The submitted file is not a PDF.')
    # Extract the text from the PDF file
    output_string = BytesIO()
    extract_text_to_fp(file, output_string)
    text = output_string.getvalue().decode('utf-8')
    
    # Create prompt with the text
    prompt_with_text = f"Create a multiple choice quiz based on the following text:\n{text}\nThe quiz should contain 10 questions, each with 4 options. The questions should be relevant and accurate based on the text.\n\nPlease include the correct answer for each question in parentheses after the option. For example, 'A) option 1 (Correct)'.\n"

    # Generate quiz questions with OpenAI API
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_with_text,
            temperature=0.7,
            max_tokens=2048,
            n = 1, # Generate only 1 quiz
            stop=None, # Generate quiz until end of text
        )
    except openai.errors.InvalidRequestError:
        abort(500, description='Failed to generate quiz questions.')

    # Extract quiz questions and options from response
    choices = response.choices[0].text.strip().split("\n\n")
    
    correct_answers = {}  # Store correct answers in a dictionary
    for i, choice in enumerate(choices):
        question, *options = choice.split("\n")
        correct_options = []
        for option in options:
            if option.endswith("(Correct)"):
                correct_options.append(option[:-10])
        questions.append({
            "question": question,
            "options": [option[:-10] if option.endswith("(Correct)") else option for option in options],
        })

        correct_answers[str(i)] = correct_options  # Add correct answers to dictionary

    # Store correct answers in the session
    session['correct_answers'] = correct_answers
    return jsonify({"quiz": questions})

@app.route('/check-answers', methods=['POST'])
def check_answers():
    answers = request.json['answers']
    results = {}
    for question_number, selected_option in answers.items():
        question_number = int(question_number) - 1  # Adjust for difference in indexing
        if selected_option is None:
            results[str(question_number + 1)] = False
        else:
            selected_option = str(selected_option) # Ensure selected_option is a string
            correct_options = session.get('correct_answers', {}).get(str(question_number), [])
            if selected_option in correct_options:
                results[str(question_number + 1)] = True
            else:
                results[str(question_number + 1)] = False
    return jsonify(results)



# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
