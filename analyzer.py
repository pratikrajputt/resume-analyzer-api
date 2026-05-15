import os
import io
import json
import re
from dotenv import load_dotenv
import PyPDF2
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

# ── LLM Setup ──────────────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

# ── PDF Extraction ──────────────────────────────────────────────────────────────
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract all text from a PDF given as raw bytes."""
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()

# ── Prompts ─────────────────────────────────────────────────────────────────────
ATS_PROMPT = PromptTemplate(
    input_variables=["resume", "jd"],
    template="""
You are an expert ATS (Applicant Tracking System) and HR specialist.

Analyze this resume against the job description and return ONLY a valid JSON object with this exact structure:
{{
  "ats_score": <integer 0-100>,
  "matched_keywords": [<list of strings>],
  "missing_keywords": [<list of strings>],
  "score_breakdown": {{
    "skills_match": <integer 0-100>,
    "experience_match": <integer 0-100>,
    "education_match": <integer 0-100>
  }}
}}

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

Return ONLY the JSON. No markdown. No explanation.
"""
)

FEEDBACK_PROMPT = PromptTemplate(
    input_variables=["resume", "jd"],
    template="""
You are a senior technical recruiter reviewing a resume.

Analyze this resume against the job description and provide structured feedback.

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

Respond in EXACTLY this format:

STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]

WEAKNESSES:
- [weakness 1]
- [weakness 2]
- [weakness 3]

IMPROVEMENTS:
- [specific improvement 1]
- [specific improvement 2]
- [specific improvement 3]

REWRITTEN SUMMARY:
[Write a 2-3 sentence professional summary optimized for this specific job description]
"""
)

# ── Main Analyzer ────────────────────────────────────────────────────────────────
def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Analyze resume against job description using two LLM chains:
    1. ATS scoring + keyword matching
    2. Detailed human-style feedback
    """

    ats_chain      = LLMChain(llm=llm, prompt=ATS_PROMPT)
    feedback_chain = LLMChain(llm=llm, prompt=FEEDBACK_PROMPT)

    # Run both chains
    ats_raw      = ats_chain.run(resume=resume_text, jd=job_description)
    feedback_raw = feedback_chain.run(resume=resume_text, jd=job_description)

    # Parse ATS JSON safely
    try:
        json_match = re.search(r'\{.*\}', ats_raw, re.DOTALL)
        ats_data   = json.loads(json_match.group()) if json_match else {}
    except Exception:
        ats_data = {
            "ats_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "score_breakdown": {}
        }

    return {
        "ats_score":         int(ats_data.get("ats_score", 0)),
        "matched_keywords":  ats_data.get("matched_keywords", []),
        "missing_keywords":  ats_data.get("missing_keywords", []),
        "score_breakdown":   ats_data.get("score_breakdown", {}),
        "detailed_feedback": feedback_raw.strip()
    }
