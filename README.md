# 🎯 AI Resume Analyzer API

> AI-powered resume analyzer built with **FastAPI + LangChain + Gemini API**

Upload a resume PDF + paste a job description → get ATS score, keyword analysis, detailed feedback, and a rewritten professional summary — all in seconds.

---

## ✨ Features

- 📊 **ATS Match Score** (0–100) with breakdown by skills, experience, education
- 🔑 **Keyword Analysis** — matched vs missing keywords from the JD
- 💡 **Detailed AI Feedback** — strengths, weaknesses, improvement suggestions
- ✍️ **Rewritten Summary** — LLM-optimized professional summary for the role
- ⚡ **REST API** — clean FastAPI backend with Swagger docs
- 🎨 **Streamlit Frontend** — interactive UI for easy testing

---

## 🏗 Architecture

```
resume PDF + job description
        ↓
  FastAPI Backend (main.py)
        ↓
  PDF Text Extraction (PyPDF2)
        ↓
  LangChain Chains (analyzer.py)
     ├── ATS Scoring Chain    → Gemini API → JSON score + keywords
     └── Feedback Chain       → Gemini API → Structured feedback
        ↓
  JSON Response to Frontend
        ↓
  Streamlit UI (frontend.py)
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/pratikrajputt/resume-analyzer-api
cd resume-analyzer-api
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up API key
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
# Get free key at: https://aistudio.google.com
```

### 4. Run the backend
```bash
python main.py
# API running at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### 5. Run the frontend (new terminal)
```bash
streamlit run frontend.py
# App running at http://localhost:8501
```

---

## 📡 API Endpoints

| Method | Endpoint   | Description              |
|--------|------------|--------------------------|
| GET    | `/`        | API info and endpoints   |
| GET    | `/health`  | Health check             |
| POST   | `/analyze` | Analyze resume vs JD     |
| GET    | `/docs`    | Swagger UI               |
| GET    | `/redoc`   | ReDoc documentation      |

### POST /analyze

**Input (multipart/form-data):**
- `resume` — PDF file
- `job_description` — string

**Output:**
```json
{
  "ats_score": 72,
  "matched_keywords": ["Python", "LangChain", "Machine Learning"],
  "missing_keywords": ["Docker", "FastAPI", "MLOps"],
  "score_breakdown": {
    "skills_match": 75,
    "experience_match": 65,
    "education_match": 80
  },
  "detailed_feedback": "STRENGTHS:\n- ...\nWEAKNESSES:\n- ...",
  "resume_text_length": 2847,
  "status": "success"
}
```

---

## 🛠 Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | FastAPI, Uvicorn, Pydantic        |
| AI/LLM    | LangChain, Gemini 1.5 Flash       |
| PDF       | PyPDF2                            |
| Frontend  | Streamlit                         |
| Env       | python-dotenv                     |

---

## 📁 Project Structure

```
resume-analyzer-api/
├── main.py           # FastAPI app — routes, validation, response models
├── analyzer.py       # LangChain logic — prompts, chains, PDF extraction
├── frontend.py       # Streamlit UI
├── requirements.txt  # Dependencies
├── .env.example      # Environment template
├── .gitignore
└── README.md
```

---

## 🌐 Deployment

### Deploy API on Railway.app (free)
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```
Add `GOOGLE_API_KEY` in Railway dashboard → Variables.

### Deploy Frontend on Streamlit Cloud (free)
1. Push to GitHub
2. Go to share.streamlit.io
3. Connect repo → set main file as `frontend.py`
4. Add `GOOGLE_API_KEY` in Streamlit secrets

---

## 👤 Author

**Prateek Singh** — AI/ML Engineer
- GitHub: [@pratikrajputt](https://github.com/pratikrajputt)
- Email: preetrajput249@gmail.com

---

## 📄 License

MIT License — feel free to use and modify
