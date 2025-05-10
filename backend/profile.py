import json
from werkzeug.utils import secure_filename
from flask import current_app
import os
from model import db, User


# Save user profile data into the database
def save_user_profile(user_id, user_data):
    user = User.query.get(user_id)
    if user:
        user.full_name = user_data.get("full_name")
        user.address = user_data.get("address")
        user.phone_number = user_data.get("phone_number")
        user.resume = user_data.get("resume")  # Save resume file name
        user.gender = user_data.get("gender")
        user.education = user_data.get("education")
        user.work_experience = user_data.get("work_experience")
        user.skills = user_data.get("skills")
        user.linkedin = user_data.get("linkedin")
        user.portfolio = user_data.get("portfolio")
        user.github = user_data.get("github")
        user.projects = user_data.get("projects")
        user.disabilities = user_data.get("disabilities")
        user.credentials = json.dumps(
            user_data.get("credentials")
        )  # Store credentials as JSON

        db.session.commit()


# Function to save the resume file
def save_resume(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        return filename
    return None


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )
