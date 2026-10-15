  ## Custom AI Chatbot with Memory

A conversational AI chatbot built with Python, Flask, and the Google Gemini API. The application maintains conversation history during an active session so that previous messages can provide context for future responses.

## Project Objective

To build a web-based AI chatbot that remembers recent conversation messages during a live session and uses them to answer relevant follow-up questions.

## Features

- AI-powered conversation
- Google Gemini API integration
- In-memory conversation history
- FIFO (First In, First Out) sliding-window memory
- Web-based chat interface
- Clear conversation functionality
- Memory status display
- Context-aware follow-up questions

## Technologies Used

- Python
- Flask
- Google Gemini API
- Google GenAI Python SDK
- HTML
- CSS
- JavaScript
- python-dotenv

## Project Structure

Generative_AI_Project_1/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── screenshots/
    ├── chatbot output.png
    ├── chatbot interface.png
    ├── demo.png
    ├── memory test.png
    ├── outputs.png
    └── Testing.png

## How to Run

1. Clone or Download the Repository

Download the project from GitHub and open the folder in VS Code.

2. Create a Virtual Environment

python -m venv .venv

3. Activate the Virtual Environment on Windows

.\.venv\Scripts\Activate.ps1

4. Install Dependencies

pip install -r requirements.txt

5. Configure Your Gemini API Key

Create a ".env" file in the project root and add your own API key:

GEMINI_API_KEY=your_api_key_here

6. Run the Application

python app.py

7. Open the Chatbot

Visit:

"http://127.0.0.1:5000"

## Screenshots

The following screenshots demonstrate the chatbot interface, generated responses, and conversation memory testing.

## Chatbot Output

"Chatbot Output" (screenshots/chatbot%20output.png)

## Chatbot Interface

"Chatbot Interface" (screenshots/chatbot%20interface.png)

## Demo

"Demo" (screenshots/demo.png)

## Memory Test

"Memory Test" (screenshots/memory%20test.png)

## Outputs

"Outputs" (screenshots/outputs.png)

## Testing

"Testing" (screenshots/Testing.png)

## Memory Management

Conversation history is maintained in a Python in-memory list while the application is running. Older messages are removed when the configured history limit is reached.

Limitation: Conversation history is temporary and is cleared when the server restarts. This project does not currently provide permanent database storage.

## Future Improvements

- Persistent memory using SQLite
- Separate conversation histories for different users
- Improved error handling and response performance
- User authentication

## Author

Developed as a Generative AI project.