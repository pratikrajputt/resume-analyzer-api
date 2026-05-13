
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

from analyzer import extract_text_from_pdf, analyze_resume

# ── App Setup ───────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Resume Analyzer API",
    description="""
## AI-Powered Resume Analyzer

Upload a resume PDF + paste a job description → get:
- **ATS Match Score** (0-100)
- **Matched & Missing Keywords**
- **Detailed Feedback** (strengths, weaknesses, improvements)
- **Rewritten Professional Summary**

Built with **FastAPI + LangChain + Gemini API**
    """,
    version="1.0.0",
    contact={
        "name": "Prateek Singh",
        "url": "https://github.com/pratikrajputt"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ── Response Model ───────────────────────────────────────────────────────────────
class ScoreBreakdown(BaseModel):
    skills_match: int = 0
    experience_match: int = 0
    education_match: int = 0

class AnalysisResult(BaseModel):
    ats_score: int
    matched_keywords: List[str]
    missing_keywords: List[str]
    score_breakdown: ScoreBreakdown
    detailed_feedback: str
    resume_text_length: int
    status: str = "success"

# ── Routes ───────────────────────────────────────────────────────────────────────
@app.get("/", tags=["General"])
def root():
    return {
        "message": "🎯 AI Resume Analyzer API is running!",
        "version": "1.0.0",
        "built_by": "Prateek Singh",
        "github": "https://github.com/pratikrajputt",
        "endpoints": {
            "analyze":    "POST /analyze  — Main endpoint",
            "health":     "GET  /health   — Health check",
            "docs":       "GET  /docs     — Swagger UI",
            "redoc":      "GET  /redoc    — ReDoc UI"
        }
    }

@app.get("/health", tags=["General"])
def health_check():
    return {
        "status":  "healthy",
        "model":   "gemini-2.5-flash",
        "powered": "LangChain + FastAPI"
    }

@app.post("/analyze", response_model=AnalysisResult, tags=["Analysis"])
async def analyze(
    resume: UploadFile = File(
        ...,
        description="Resume as PDF file"
    ),
    job_description: str = Form(
        ...,
        description="Full job description text"
    )
):
    """
    ## Analyze Resume Against Job Description

    **Input:**
    - `resume` — PDF file of the resume
    - `job_description` — Full text of the job description

    **Returns:**
    - ATS match score (0-100)
    - Matched and missing keywords
    - Score breakdown by category
    - Detailed AI feedback with improvement suggestions
    - Rewritten professional summary
    """

    # ── Validations ────────────────────────────────────────────────────────────
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported. Please upload a .pdf file."
        )

    if len(job_description.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Job description is too short. Please provide the full job description."
        )

    # ── Process ────────────────────────────────────────────────────────────────
    try:
        pdf_bytes   = await resume.read()
        resume_text = extract_text_from_pdf(pdf_bytes)

        if not resume_text or len(resume_text) < 100:
            raise HTTPException(
                status_code=400,
                detail="Could not extract readable text from PDF. Please ensure the PDF is not scanned/image-based."
            )

        result = analyze_resume(resume_text, job_description)

        breakdown = ScoreBreakdown(
            skills_match     = result["score_breakdown"].get("skills_match", 0),
            experience_match = result["score_breakdown"].get("experience_match", 0),
            education_match  = result["score_breakdown"].get("education_match", 0)
        )

        return AnalysisResult(
            ats_score         = result["ats_score"],
            matched_keywords  = result["matched_keywords"],
            missing_keywords  = result["missing_keywords"],
            score_breakdown   = breakdown,
            detailed_feedback = result["detailed_feedback"],
            resume_text_length= len(resume_text),
            status            = "success"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# ── Run ──────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
