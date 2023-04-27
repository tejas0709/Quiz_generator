PDF Quiz Generator

This is a Flask web application that generates a multiple-choice quiz based on the text from a PDF file. The quiz contains 10 questions, each with 4 options, and each option has a correct answer.

Getting Started

To run this application, follow these steps:

    Clone this repository: git clone https://github.com/your-username/pdf-quiz-generator.git
    Move your documents(pdf) to the tmp directory
    Replace YOUR_API_KEY with your OpenAI API key in the app.py(with " ")
    Install the required packages: pip install -r requirements.txt
    Set the FLASK_APP environment variable to app.py: $env:FLASK_APP = "app.py"     
    Run the application: flask run
    Open the application in a web browser at http://127.0.0.1:5000

Usage

    Upload a PDF file by clicking on the "Choose File" button and selecting the file from your computer.
    Click the "Generate Quiz" button to generate a quiz based on the text from the PDF file.
    Answer the quiz questions by selecting the option you believe to be correct for each question.
    Click the "Submit" button to see which questions you answered correctly and which ones you did not.

Dependencies

This application relies on the following dependencies:

    Flask
    requests
    openai
    pdfminer.six

These dependencies are listed in the requirements.txt file and can be installed with pip.
API Keys

This application requires an OpenAI API key to generate quiz questions. The API key should be set as an environment variable named OPENAI_API_KEY.
Contributing

If you find a bug or have a suggestion for a new feature, please open an issue or submit a pull request. We welcome contributions from the community!
