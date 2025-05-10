

# 🧠 AvsarAI — AI-Powered Job Application Assistant

AvsarAI automates the process of applying to jobs using AI agents that interact with websites through a browser. It features a secure authentication system, user profile management, and AI-driven resume submission using Google Gemini and Playwright.

## 🚀 Features

* ✅ User registration and authentication
* 📝 Profile management with resume upload
* 🤖 AI agent that automates job applications
* 🌐 Browser automation with Playwright
* 🧠 Google Gemini-powered form filling
* 🔐 Secure credential handling (via `.env`)
* 🌍 CORS-enabled frontend-backend integration
* 🌈 Frontend built with Vite + Vue + TypeScript
---

## ⚙️ Installation

### 🧠 Prerequisites

* Python 3.8+
* Node.js 16+
* Playwright (installed via Python)
* Google Gemini API access

### 🐍 Backend (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your GOOGLE_CREDENTIALS_JSON and other secrets

# Initialize database
python app.py
```

### 🌐 Frontend (Vue)

```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 Environment Variables (`.env`)

```
GOOGLE_CREDENTIALS_JSON=your_google_api_credentials
SECRET_KEY=your_flask_secret
```

---

## 🧠 AI Agent

The AI agent uses Google Gemini (via `langchain_google_genai`) to:

1. Navigate to a given job URL
2. Fill out the application form using user profile data
3. Upload the resume
4. Submit the application

All this happens asynchronously inside a real Chromium browser (via Playwright).

---
## 📁 Project Structure

```bash
├── backend/
│   ├── api.py               # Main Flask app and API routes
│   ├── app.py               # App bootstrapper
│   ├── model.py             # SQLAlchemy models
│   ├── profile.py           # Resume and profile utilities
│   ├── config.py            # App configuration
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   ├── router.ts
│   │   └── components/
│   │       ├── Login.vue
│   │       ├── Register.vue
│   │       ├── Profile.vue
│   │       └── Apply.vue
│   └── ...
├── uploads/                 # Uploaded resumes
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md
```

## 🙌 Acknowledgments

* [Flask](https://flask.palletsprojects.com/)
* [Vue.js](https://vuejs.org/)
* [Playwright](https://playwright.dev/)
* [Langchain](https://www.langchain.com/)
* [Google Generative AI](https://ai.google/discover/generativeai)

---

