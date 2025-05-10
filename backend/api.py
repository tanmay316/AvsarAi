from flask import Flask, request, jsonify, copy_current_request_context, current_app
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User, JobApplication
from profile import save_user_profile, save_resume
from flask_login import LoginManager
from flask_migrate import Migrate
from config import UPLOAD_FOLDER
from flask_cors import CORS
from browser_use import Agent, Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import asyncio
from threading import Thread
import json
import uuid
import datetime
import time
import os
# Add at the top of your file
import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()  # Load the environment variables from the .env file

# Access the variables
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])  # Enable CORS with credentials
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and login manager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Initialize Flask-Migrate
migrate = Migrate(app, db)

ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = 'uploads' 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# JobApplicationAgent class for browser automation
class JobApplicationAgent:
    def __init__(self, user, job_url):
        self.user = user
        self.job_url = job_url
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
        
        self.system_prompt = f"""
        You are an AI job application assistant. Follow these steps:
        1. Navigate to {self.job_url}
        2. Login using credentials: {self._masked_credentials()}
        3. Fill form with:
           - Name: {self.user.full_name}
           - Email: {self.user.email}
           - Phone: {self.user.phone_number}
           - Education: {self.user.education}
           - Experience: {self.user.work_experience}
        4. Upload resume from: {self.user.resume}
        5. Handle multi-page forms
        """

    def _masked_credentials(self):
        return {k: f"<secret>{k}</secret>" for k in json.loads(self.user.credentials).keys()}

    async def run_agent(self, browser):
        async with await browser.new_context() as context:
            agent = Agent(
                task=self.system_prompt,
                llm=self.llm,
                use_vision=True,
                browser_context=context,
                sensitive_data=json.loads(self.user.credentials),
                extend_system_message="""SPECIAL INSTRUCTIONS:
                    - Preserve session cookies
                    - Use CSS selectors for reliable input
                    - Handle CAPTCHAs via user interaction"""
            )
            return await agent.run()
# Add debug logging
from playwright.async_api import async_playwright

# async def test_browser():
#     async with async_playwright() as p:
#         print("Chromium path:", p.chromium.executable_path)
#         browser = await p.chromium.launch()
#         page = await browser.new_page()
#         await page.goto('https://example.com')
#         await browser.close()

# # Run this once to verify
# asyncio.run(test_browser())
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    print("Chromium path:", p.chromium.executable_path)



# Registration API
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(
        username=name,
        email=email,
        password=generate_password_hash(password),
        full_name="",
        address="",
        phone_number="",
        gender="",
        education="",
        work_experience="",
        skills="",
        linkedin="",
        portfolio="",
        github="",
        projects="",
        disabilities="",
        credentials=json.dumps({"gmail": "", "password": ""})
    )
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return jsonify({
        "message": "Registration successful",
        "user_id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }), 201

# Login API
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401

# Profile API
@app.route("/api/profile", methods=["GET"])
@login_required
def get_profile():
    user = current_user
    profile_data = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "address": user.address,
        "phone_number": user.phone_number,
        "resume": user.resume,
        "gender": user.gender,
        "education": user.education,
        "work_experience": user.work_experience,    
        "skills": user.skills,  
        "linkedin": user.linkedin,       
        "portfolio": user.portfolio,
        "github": user.github,
        "projects": user.projects,
        "disabilities": user.disabilities,
        "credentials": json.loads(user.credentials)  # Convert string back to dict
    }
    return jsonify(profile_data), 200


@app.route("/api/profile", methods=["POST"])
@login_required
def profile():
    if 'resume' in request.files:
        resume = request.files['resume']
        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(resume_path)
            current_user.resume = resume_path  # Save the path to the user's profile in the database
            db.session.commit()

    # Now update other profile fields
    data = request.form  # Use form to get non-file data
    current_user.full_name = data.get('full_name')
    current_user.address = data.get('address')
    current_user.phone_number = data.get('phone_number')
    current_user.gender = data.get('gender')
    current_user.education = data.get('education')
    current_user.work_experience = data.get('work_experience')
    current_user.skills = data.get('skills')
    current_user.linkedin = data.get('linkedin')
    current_user.portfolio = data.get('portfolio')
    current_user.github = data.get('github')
    current_user.projects = data.get('projects')
    current_user.disabilities = data.get('disabilities')

    # If you are using credentials, save them here as well
    credentials = {
        'gmail': data.get('gmail'),
        'password': data.get('password')
    }
    current_user.credentials = json.dumps(credentials)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

from werkzeug.utils import secure_filename
import os

@app.route("/api/upload_resume", methods=["POST"])
@login_required
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file found"}), 400
    
    resume = request.files["resume"]
    if resume.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(resume.filename)
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    resume.save(resume_path)
    
    current_user.resume = resume_path  # Save the file path to the user's profile
    db.session.commit()
    
    return jsonify({"message": "Resume uploaded successfully", "resume_path": resume_path}), 200


# Apply API
@app.route("/api/apply", methods=["POST"])
@login_required
def apply():
    data = request.json
    job_url = data.get("job_url")
    
    if not job_url:
        return jsonify({"error": "Job URL is required"}), 400
    
    application_id = str(uuid.uuid4())
    
    # Save the job application to the database
    job_application = JobApplication(
        id=application_id,
        user_id=current_user.id,
        job_url=job_url,
        status="processing",
        timestamp=datetime.datetime.now()
    )

    db.session.add(job_application)
    db.session.commit()

    @copy_current_request_context  # Preserve request context
    def async_wrapper(app_id, user_id, url):
        # Create new application context for the thread
        with app.app_context():
            try:
                # Load user from database within context
                user = User.query.get(user_id)
                
                # Initialize browser within context
                browser = Browser(
                    config=BrowserConfig(
                        browser_binary_path=None,  # Let Playwright manage the browser
                        channel="chromium",
                        headless=False,
                        stealth_mode=True
                    )
                )

                
                agent = JobApplicationAgent(user, url)
                result = asyncio.run(agent.run_agent(browser))

                # Update the job application status to 'completed' and store the result
                job_application = JobApplication.query.get(app_id)
                job_application.status = "completed"
                job_application.result = result
                db.session.commit()
            except Exception as e:
                # Update status and store error message if any issue occurs
                job_application = JobApplication.query.get(app_id)
                job_application.status = "failed"
                job_application.error = str(e)
                db.session.commit()
            finally:
                if 'browser' in locals():
                    asyncio.run(browser.close())

    Thread(target=async_wrapper, args=(application_id, current_user.id, job_url)).start()
    
    return jsonify({
        "message": "AI agent started job application",
        "application_id": application_id
    }), 200

# Application Status API
@app.route("/api/apply/status/<application_id>", methods=["GET"])
@login_required
def get_application_status(application_id):
    # Get the application from the database
    application = JobApplication.query.get(application_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404

    # Ensure the user querying the status is the same as the user who created the application
    if application.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({
        "status": application.status,
        "error": application.error
    }), 200

# Cancel Application API
@app.route("/api/apply/cancel", methods=["POST"])
@login_required
def cancel_application():
    data = request.get_json()
    application_id = data.get("application_id")
    
    if not application_id or application_id not in job_applications:
        return jsonify({"error": "Application not found"}), 404
    
    application = job_applications[application_id]
    if application["user_id"] != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    if application["status"] in ["completed", "cancelled"]:
        return jsonify({"error": "Cannot cancel application in current state"}), 400
    
    application["status"] = "cancelled"
    return jsonify({"message": "Application cancelled successfully"}), 200

# Logout API
@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
