from flask import Blueprint, request, jsonify
import google.generativeai as genai
import mysql.connector
import logging
from db import get_db_connection
from config import Config

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

# Set up logging
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Blueprint for chatbot routes
chatbot_bp = Blueprint("chatbot", __name__)


def check_cache(user_input):
    """Check if response exists in cache."""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT response FROM cache WHERE query = %s", (user_input,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else None
    except mysql.connector.Error as db_err:
        logging.error(f"Database Error (Cache Check): {db_err}")
        return None


def save_to_cache(user_input, response):
    """Save response to cache for future queries."""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cache (query, response) VALUES (%s, %s)",
                (user_input, response),
            )
            conn.commit()
            cursor.close()
            conn.close()
    except mysql.connector.Error as db_err:
        logging.error(f"Database Error (Saving Cache): {db_err}")


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    """Chatbot endpoint to process user messages and return AI responses."""
    try:
        data = request.json
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        # Check cache first
        cached_response = check_cache(user_input)
        if cached_response:
            return jsonify({"response": cached_response, "cached": True})

        # Call Gemini API
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(user_input)

        # Extract and validate AI response
        bot_response = response.text if hasattr(response, "text") else None
        if not bot_response:
            return jsonify({"error": "Invalid AI response"}), 500

        # Cache response for future queries
        save_to_cache(user_input, bot_response)

        return jsonify({"response": bot_response, "cached": False})

    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
