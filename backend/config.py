# AIzaSyCUzs3vHLia1cLKWPzrSfpotELjLjosf9U

import os


class Config:
    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY", "AIzaSyD4sJcSpHnzSEEQpGcxdff7aw4gdwzYyzs"
    )

    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
    MYSQL_DB = os.getenv("MYSQL_DB", "chatbot_db")

    DEBUG = os.getenv("DEBUG", "True") == "True"
    LOG_FILE = "logs/chatbot.log"
