import os
from dotenv import load_dotenv

load_dotenv()

# Sensitive Information - Passwords should not be exposed in the codebase
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///users.db")  # SQLite path

# Default configurations
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}  # For resumes
