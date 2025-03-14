from flask import Flask
from flask_cors import CORS
from routes import chatbot_bp

app = Flask(__name__)
CORS(app)

# Register Blueprint
app.register_blueprint(chatbot_bp, url_prefix="/api")

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Something went wrong, please try again later"}, 500

if __name__ == "__main__":
    app.run(debug=True)
