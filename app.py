from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )

app = Flask(__name__)

# Gemini client: reduce extra waiting from automatic retries
client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=30000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)

# In-memory conversation history
conversation_history = []

# Maximum number of messages retained
MAX_HISTORY_MESSAGES = 100

# Fast, lightweight Gemini model
MODEL_NAME = "gemini-3.5-flash-lite"

SYSTEM_INSTRUCTION = """
You are a helpful conversational AI chatbot with memory.

Instructions:
1. Answer the user's CURRENT message first.
2. Use previous conversation history only when relevant.
3. Do not answer an old question instead of the current question.
4. Remember details present in the available conversation history.
5. Do not claim to remember information that is not in the history.
6. Do not mention conversation history unless the user asks about it.
7. Give clear, accurate, useful answers.
8. Keep responses reasonably concise unless more detail is requested.
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Invalid request. Please send a message."
            }), 400

        user_message = data.get("message", "")

        if not isinstance(user_message, str):
            return jsonify({
                "error": "Message must be text."
            }), 400

        user_message = user_message.strip()

        if not user_message:
            return jsonify({
                "error": "Please enter a message."
            }), 400

        # Add the current message to a temporary history.
        user_content = types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        )

        request_history = conversation_history + [user_content]

        # Keep complete user/assistant pairs when trimming history.
        while len(request_history) > MAX_HISTORY_MESSAGES:
            del request_history[:2]

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=request_history,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.5,
                    max_output_tokens=512,
                    thinking_config=types.ThinkingConfig(
                        thinking_level="low"
                    )
                )
            )

        except Exception as error:
            error_text = str(error)
            error_upper = error_text.upper()

            print("\n" + "=" * 60)
            print("GEMINI API ERROR")
            print(error_text)
            print("=" * 60 + "\n")

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_upper
                or "QUOTA" in error_upper
            ):
                return jsonify({
                    "error": (
                        "Gemini API quota is exhausted or rate-limited. "
                        "Wait for your quota to reset and try again."
                    )
                }), 429

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_upper
                or "502" in error_text
            ):
                return jsonify({
                    "error": (
                        "Gemini is temporarily unavailable. "
                        "Please try again shortly."
                    )
                }), 503

            if (
                "TIMEOUT" in error_upper
                or "TIMED OUT" in error_upper
                or "DEADLINE EXCEEDED" in error_upper
            ):
                return jsonify({
                    "error": (
                        "Gemini did not respond within the time limit. "
                        "Please try again."
                    )
                }), 504

            return jsonify({
                "error": (
                    "Gemini request failed. Check the VS Code terminal "
                    "for details and verify your API configuration."
                )
            }), 500

        # Validate the generated response.
        ai_response = response.text

        if not ai_response:
            return jsonify({
                "error": (
                    "Gemini returned an empty response. "
                    "Please try a different question."
                )
            }), 502

        # Save the conversation only after a successful response.
        conversation_history.append(user_content)

        conversation_history.append(
            types.Content(
                role="model",
                parts=[types.Part(text=ai_response)]
            )
        )

        # Retain only the latest complete conversation pairs.
        while len(conversation_history) > MAX_HISTORY_MESSAGES:
            del conversation_history[:2]

        return jsonify({
            "response": ai_response,
            "history_count": len(conversation_history)
        })

    except Exception as error:
        print("UNEXPECTED ERROR:", error)

        return jsonify({
            "error": "An unexpected error occurred. Please try again."
        }), 500


@app.route("/clear", methods=["POST"])
def clear_conversation():
    conversation_history.clear()

    return jsonify({
        "message": "Conversation cleared successfully."
    })


@app.route("/memory", methods=["GET"])
def memory_status():
    return jsonify({
        "messages_in_memory": len(conversation_history),
        "max_messages": MAX_HISTORY_MESSAGES
    })


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("       PROJECT 1 - CUSTOM AI CHATBOT")
    print("              WITH MEMORY")
    print("=" * 60)
    print("Server  : http://127.0.0.1:5000")
    print("Memory  : ACTIVE")
    print("Model   : " + MODEL_NAME)
    print("Thinking: LOW")
    print("Timeout : 30 seconds")
    print("=" * 60)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )