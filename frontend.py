import streamlit as st
import requests

# ── Page Config ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0;
    }
    .score-card {
        text-align: center;
        padding: 2.5rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    .keyword-match {
        background: #28a745;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        display: inline-block;
        margin: 4px;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.2);
    }
    .keyword-miss {
        background: #dc3545;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        display: inline-block;
        margin: 4px;
        box-shadow: 0 2px 8px rgba(220, 53, 69, 0.2);
    }
    .feedback-box {
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border-left: 5px solid;
        line-height: 1.8;
        font-size: 15px;
        color: #1a1a1a;
    }
    .feedback-strengths {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left-color: #28a745;
    }
    .feedback-weaknesses {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        border-left-color: #ffc107;
    }
    .feedback-improvements {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left-color: #17a2b8;
    }
    .feedback-summary {
        background: linear-gradient(135deg, #e7e8ea 0%, #d9dadd 100%);
        border-left-color: #6c757d;
    }
    .feedback-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .feedback-content {
        color: #2c3e50;
        line-height: 1.7;
    }
    .feedback-content li {
        margin: 0.5rem 0;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.875rem;
        font-size: 16px;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    .input-section-title {
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🎯 AI Resume Analyzer</h1>
    <p>Powered by FastAPI + LangChain + Gemini AI</p>
    <p style="font-size:13px;opacity:0.8">Built by Prateek Singh · github.com/pratikrajputt</p>
</div>
""", unsafe_allow_html=True)

# ── Input Section ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="input-section-title">📄 Upload Your Resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader(
        "Drop your resume here (PDF only)",
        type=["pdf"],
        help="Make sure your PDF has selectable text (not a scanned image)"
    )
    if resume_file:
        st.success(f"✅ {resume_file.name} uploaded ({round(len(resume_file.getvalue())/1024, 1)} KB)")

with col2:
    st.markdown('<div class="input-section-title">💼 Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste the full job description",
        height=220,
        placeholder="Paste the complete job description here including required skills, responsibilities, and qualifications...",
        help="The more complete the JD, the more accurate the analysis"
    )
    if job_description:
        word_count = len(job_description.split())
        st.caption(f"📝 {word_count} words")

st.markdown("---")

# ── Analyze Button ───────────────────────────────────────────────────────────────
analyze_clicked = st.button("🚀 Analyze My Resume", type="primary")

if analyze_clicked:
    if not resume_file:
        st.error("⚠️ Please upload your resume PDF first")
    elif not job_description or len(job_description.strip()) < 50:
        st.error("⚠️ Please paste a complete job description (at least 50 characters)")
    else:
        with st.spinner("🤖 AI is analyzing your resume... This may take 15-30 seconds"):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    files={
                        "resume": (
                            resume_file.name,
                            resume_file.getvalue(),
                            "application/pdf"
                        )
                    },
                    data={"job_description": job_description},
                    timeout=60
                )

                # ── Results ──────────────────────────────────────────────────────
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Analysis Complete!")
                    st.markdown("---")

                    # ── ATS Score ─────────────────────────────────────────────────
                    score = data["ats_score"]
                    if score >= 75:
                        score_color = "#28a745"
                        score_label = "Excellent Match! 🎉"
                        score_msg   = "Your resume is well-optimized for this role."
                    elif score >= 55:
                        score_color = "#fd7e14"
                        score_label = "Good Match 👍"
                        score_msg   = "A few improvements could significantly boost your chances."
                    else:
                        score_color = "#dc3545"
                        score_label = "Needs Work ⚠️"
                        score_msg   = "Your resume needs optimization for this specific role."

                    st.markdown(f"""
                    <div class="score-card" style="background: {score_color}15; border: 2px solid {score_color}">
                        <h1 style="color:{score_color};font-size:80px;margin:0">{score}</h1>
                        <h3 style="color:{score_color};margin:0">/ 100 — {score_label}</h3>
                        <p style="color:#666;margin-top:8px">{score_msg}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Score Breakdown ───────────────────────────────────────────
                    st.markdown("### 📊 Score Breakdown")
                    bd = data.get("score_breakdown", {})
                    c1, c2, c3 = st.columns(3)
                    c1.metric("🛠 Skills Match",      f"{bd.get('skills_match', 0)}%")
                    c2.metric("💼 Experience Match",  f"{bd.get('experience_match', 0)}%")
                    c3.metric("🎓 Education Match",   f"{bd.get('education_match', 0)}%")

                    st.markdown("---")

                    # ── Keywords ──────────────────────────────────────────────────
                    st.markdown("### 🔑 Keyword Analysis")
                    kc1, kc2 = st.columns(2)

                    with kc1:
                        st.markdown("**✅ Matched Keywords**")
                        matched = data.get("matched_keywords", [])
                        if matched:
                            kw_html = " ".join([f'<span class="keyword-match">{k}</span>' for k in matched])
                            st.markdown(kw_html, unsafe_allow_html=True)
                        else:
                            st.info("No strong keyword matches found")

                    with kc2:
                        st.markdown("**❌ Missing Keywords**")
                        missing = data.get("missing_keywords", [])
                        if missing:
                            kw_html = " ".join([f'<span class="keyword-miss">{k}</span>' for k in missing])
                            st.markdown(kw_html, unsafe_allow_html=True)
                            st.caption("💡 Add these keywords naturally into your resume")
                        else:
                            st.success("No critical keywords missing!")

                    st.markdown("---")

                    # ── Detailed Feedback ─────────────────────────────────────────
                    st.markdown("### 🤖 AI Feedback & Recommendations")
                    feedback = data.get("detailed_feedback", "")

                    # Parse sections
                    sections = {
                        "STRENGTHS":           ("✅ Strengths",                    "feedback-strengths"),
                        "WEAKNESSES":          ("⚠️ Weaknesses",                   "feedback-weaknesses"),
                        "IMPROVEMENTS":        ("💡 Improvement Suggestions",      "feedback-improvements"),
                        "REWRITTEN SUMMARY":   ("✍️ Rewritten Professional Summary","feedback-summary")
                    }

                    current_section = None
                    section_content = {}

                    for line in feedback.split("\n"):
                        line = line.strip()
                        matched_section = False
                        for key in sections:
                            if line.startswith(key + ":") or line == key:
                                current_section = key
                                section_content[key] = []
                                matched_section = True
                                break
                        if not matched_section and current_section and line:
                            section_content[current_section].append(line)

                    for key, (title, css_class) in sections.items():
                        if key in section_content and section_content[key]:
                            content = "<br>".join(section_content[key])
                            st.markdown(f"""
                            <div class="feedback-box {css_class}">
                                <div class="feedback-title">{title}</div>
                                <div class="feedback-content">{content}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("---")
                    st.caption(f"📋 Resume text extracted: {data.get('resume_text_length', 0)} characters | Model: Gemini 2.5 Flash")

                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"❌ API Error: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to API backend. Make sure FastAPI is running: `python main.py`")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# ── Footer ────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#888;font-size:13px">
    Built with ❤️ using FastAPI + LangChain + Gemini AI &nbsp;|&nbsp;
    <a href="https://github.com/pratikrajputt" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)
