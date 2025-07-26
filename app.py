import streamlit as st
from services.parser import extract_text_from_pdf, parse_resume, parse_job_description
from services.scorer import score_match
from services.langchain_matcher import analyze_match_with_llm
from services.ats_matcher import get_keyword_overlap
from services.pdf_reporter import generate_pdf_report
from dotenv import load_dotenv

load_dotenv()

# --------- PAGE SETUP ---------
st.set_page_config(
    page_title="🚀 Smart Resume Analyzer & Job Match Scorer",
    page_icon="📄",
    layout="wide"
)

# --------- CUSTOM HEADER & DARK THEME ---------
st.markdown(
    """
    <style>
        /* Dark Background Theme */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #ffffff;
        }
        
        /* Main containers */
        .main .block-container {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 20px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Header styling */
        .main-title {
            text-align: center;
            font-size: 3.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, #00d4ff, #6c63ff, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
        }
        
        .sub-title {
            text-align: center;
            font-size: 1.3rem;
            color: #a0a0a0;
            margin-bottom: 40px;
            font-weight: 300;
        }
        
        /* Column styling */
        .stColumn {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin: 0.5rem;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #00d4ff !important;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        }
        
        /* File uploader */
        .stFileUploader {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            border: 2px dashed rgba(0, 212, 255, 0.3);
            padding: 1rem;
        }
        
        /* Text area */
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 212, 255, 0.3) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            font-size: 1rem !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(45deg, #00d4ff, #6c63ff) !important;
            border: none !important;
            border-radius: 25px !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 1.1rem !important;
            padding: 0.75rem 2rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4) !important;
        }
        
        .stDownloadButton > button {
            background: linear-gradient(45deg, #ff6b6b, #ffa726) !important;
            border: none !important;
            border-radius: 25px !important;
            color: white !important;
            font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
        }
        
        /* Metrics */
        .metric-container {
            background: rgba(0, 212, 255, 0.1);
            border-radius: 15px;
            padding: 1.5rem;
            border: 1px solid rgba(0, 212, 255, 0.3);
            text-align: center;
        }
        
        /* Progress bar */
        .stProgress .st-bo {
            background: linear-gradient(90deg, #00d4ff, #6c63ff);
            border-radius: 10px;
        }
        
        /* Success and error messages */
        .stSuccess {
            background: rgba(76, 175, 80, 0.1) !important;
            border: 1px solid rgba(76, 175, 80, 0.3) !important;
            border-radius: 10px !important;
        }
        
        .stError {
            background: rgba(244, 67, 54, 0.1) !important;
            border: 1px solid rgba(244, 67, 54, 0.3) !important;
            border-radius: 10px !important;
        }
        
        .stWarning {
            background: rgba(255, 193, 7, 0.1) !important;
            border: 1px solid rgba(255, 193, 7, 0.3) !important;
            border-radius: 10px !important;
            color: #ffc107 !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            border: 1px solid rgba(0, 212, 255, 0.3) !important;
            color: #00d4ff !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(255, 255, 255, 0.02) !important;
            border-radius: 0 0 10px 10px !important;
            border: 1px solid rgba(0, 212, 255, 0.2) !important;
        }
        
        /* Divider */
        hr {
            border: 1px solid rgba(0, 212, 255, 0.3) !important;
            margin: 2rem 0 !important;
        }
        
        /* Spinner */
        .stSpinner {
            color: #00d4ff !important;
        }
        
        /* General text */
        .stMarkdown {
            color: #ffffff !important;
        }
        
        /* Sidebar (if used) */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.05) !important;
        }
        
        /* Custom glow effect for important elements */
        .glow-effect {
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
            border: 1px solid rgba(0, 212, 255, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">📄 Smart Resume Analyzer & Job Match Scorer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Get AI-powered feedback and ATS optimization for your resume instantly</div>', unsafe_allow_html=True)

# --------- LAYOUT ---------
col1, col2 = st.columns(2)

with col1:
    st.header("📤 Upload Resume")
    resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

with col2:
    st.header("📝 Paste Job Description")
    job_text = st.text_area("Paste the job description here", height=220)

# --------- PROCESSING ---------
if resume_file and job_text:
    with st.spinner("🔍 Parsing resume..."):
        resume_text = extract_text_from_pdf(resume_file)
        resume_data = parse_resume(resume_text)

    with st.spinner("🧾 Parsing job description..."):
        job_data = parse_job_description(job_text)

    with st.spinner("📊 Scoring resume match..."):
        result = score_match(resume_data, job_data)

    with st.spinner("🧠 Analyzing with LLM (Groq)..."):
        gpt_feedback = analyze_match_with_llm(resume_text, job_text)

    with st.spinner("📌 Comparing keywords (ATS Simulation)..."):
        ats = get_keyword_overlap(resume_text, job_text)

    # --------- RESULTS DISPLAY ---------
    st.markdown("## 📈 Results Summary")

    colA, colB = st.columns([1, 2])
    with colA:
        st.metric("🎯 Match Score", f"{result['match_score']}%")
        st.progress(result["match_score"] / 100)

    with colB:
        st.markdown("**✅ Matched Skills:**")
        st.success(", ".join(result["matched_skills"]) or "No matched skills")

        st.markdown("**❌ Missing Skills:**")
        st.error(", ".join(result["missing_skills"]) or "None")

    # Divider
    st.markdown("---")

    # --------- GROQ LLM FEEDBACK ---------
    with st.expander("🤖 AI-Powered Feedback (Groq LLaMA 3)", expanded=True):
        for line in gpt_feedback.strip().split('\n'):
            if line.strip():  # Only show lines that have content
                st.write(f"🟦 {line}")
            else:
                st.write("")  # Show empty line without the emoji

    # Divider
    st.markdown("---")

    # --------- ATS KEYWORD ANALYSIS ---------
    st.subheader("📊 ATS Keyword Coverage")
    st.metric("Coverage %", f"{ats['coverage_percent']}%")

    with st.expander("🔑 Matched Keywords"):
        st.write(", ".join(ats["matched_keywords"]) or "No keywords matched.")

    with st.expander("📌 Top Keywords in Resume"):
        for word, count in ats["top_resume_keywords"]:
            st.write(f"{word} — {count} times")

    with st.expander("📌 Top Keywords in Job Description"):
        for word, count in ats["top_jd_keywords"]:
            st.write(f"{word} — {count} times")

    # Divider
    st.markdown("---")

    # --------- PDF REPORT ---------
    st.subheader("📥 Download GPT Analysis as PDF")
    if st.button("Generate PDF Report"):
        path = generate_pdf_report(gpt_feedback)
        with open(path, "rb") as f:
            st.download_button("⬇️ Download GPT Match Report (PDF)", f, file_name="gpt_match_report.pdf")

else:
    st.warning("📂 Please upload a resume and paste a job description to get started.")