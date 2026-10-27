import sys
import html
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.graph import analyze_job_description
from core.export import report_to_json

st.set_page_config(page_title="AI Job Description Analyzer", page_icon="✨", layout="centered")

SAMPLE = (
    "ABC Technologies is hiring an AI Engineer for a full-time on-site role. "
    "We need 2-4 years of experience. You will build agentic workflows. "
    "Required: Python, FastAPI, LangGraph, SQL. Strong communication, teamwork "
    "and problem solving skills are expected."
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Poppins', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(99,102,241,0.35) 0%, transparent 38%),
        radial-gradient(circle at 88% 18%, rgba(236,72,153,0.25) 0%, transparent 35%),
        radial-gradient(circle at 50% 95%, rgba(20,184,166,0.20) 0%, transparent 40%),
        #0a0c18;
}
#MainMenu, footer, .stDeployButton { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 880px; padding-top: 2.5rem; padding-bottom: 4rem; }

/* ---------- Hero ---------- */
.hero { text-align: center; margin-bottom: 1.6rem; }
.badge {
    display: inline-block; padding: 6px 16px; border-radius: 999px;
    background: rgba(99,102,241,0.15); border: 1px solid rgba(129,140,248,0.4);
    color: #c7d2fe; font-size: 0.78rem; font-weight: 500; letter-spacing: .5px;
}
.hero h1 {
    font-size: 3rem; font-weight: 800; margin: 14px 0 6px 0; line-height: 1.15;
    background: linear-gradient(90deg, #818cf8, #f472b6, #2dd4bf);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: #94a3b8; font-size: 1rem; margin: 0; }

/* ---------- Pipeline ---------- */
.pipeline { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin: 1.2rem 0 1.8rem 0; }
.step {
    display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 12px;
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    color: #cbd5e1; font-size: 0.78rem; font-weight: 500;
}
.step .num {
    width: 20px; height: 20px; border-radius: 50%; display: inline-flex; align-items: center;
    justify-content: center; font-size: 0.68rem; font-weight: 700; color: white;
    background: linear-gradient(135deg, #6366f1, #ec4899);
}
.arrow { color: #475569; align-self: center; }

/* ---------- Input ---------- */
.stTextArea label { color: #e2e8f0 !important; font-weight: 600; }
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important; color: #f1f5f9 !important;
    border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 16px !important;
    padding: 16px !important; font-size: 0.95rem !important;
}
.stTextArea textarea:focus { border-color: #818cf8 !important; box-shadow: 0 0 0 3px rgba(129,140,248,0.25) !important; }

/* ---------- Buttons ---------- */
.stButton > button {
    border-radius: 14px; font-weight: 600; padding: 0.6rem 1.4rem; border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.05); color: #e2e8f0; transition: all .2s ease;
}
.stButton > button:hover { border-color: #818cf8; color: white; transform: translateY(-1px); }
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6366f1, #ec4899); border: none; color: white;
    box-shadow: 0 8px 24px rgba(99,102,241,0.35);
}
.stButton > button[kind="primary"]:hover { box-shadow: 0 10px 30px rgba(236,72,153,0.45); }
.stDownloadButton > button {
    width: 100%; border-radius: 14px; font-weight: 600; padding: 0.7rem; border: none; color: white;
    background: linear-gradient(90deg, #14b8a6, #6366f1); box-shadow: 0 8px 24px rgba(20,184,166,0.3);
}

/* ---------- Result cards ---------- */
.glass {
    background: rgba(255,255,255,0.045); border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px; padding: 20px 22px; margin-bottom: 16px; backdrop-filter: blur(10px);
}
.sec-title {
    color: #94a3b8; font-size: 0.74rem; font-weight: 600; letter-spacing: 1.4px;
    text-transform: uppercase; margin-bottom: 12px;
}
.report-head { text-align: center; margin: 2rem 0 1rem 0; }
.report-head h2 { color: #f8fafc; font-weight: 700; margin: 0; font-size: 1.6rem; }
.report-head span { color: #94a3b8; font-size: 0.9rem; }

.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.stat { background: rgba(255,255,255,0.04); border-radius: 14px; padding: 14px 16px; border-left: 3px solid #818cf8; }
.stat:nth-child(2) { border-left-color: #f472b6; }
.stat:nth-child(3) { border-left-color: #2dd4bf; }
.stat:nth-child(4) { border-left-color: #fbbf24; }
.stat .k { color: #94a3b8; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; }
.stat .v { color: #f8fafc; font-size: 1.1rem; font-weight: 600; margin-top: 4px; }

.pills { margin-top: 14px; }
.pill {
    display: inline-block; padding: 6px 14px; margin: 0 8px 0 0; border-radius: 999px;
    background: rgba(99,102,241,0.18); color: #c7d2fe; border: 1px solid rgba(129,140,248,0.35);
    font-size: 0.82rem; font-weight: 500;
}
.pill.pink { background: rgba(236,72,153,0.15); color: #fbcfe8; border-color: rgba(244,114,182,0.35); }

/* ---------- Tags ---------- */
.tag {
    display: inline-block; padding: 6px 14px; margin: 0 8px 8px 0; border-radius: 999px;
    font-size: 0.83rem; font-weight: 500; border: 1px solid transparent;
}
.tag.req  { background: rgba(168,85,247,0.15); color: #e9d5ff; border-color: rgba(192,132,252,0.35); }
.tag.tech { background: rgba(59,130,246,0.15); color: #bfdbfe; border-color: rgba(96,165,250,0.35); }
.tag.soft { background: rgba(34,197,94,0.15);  color: #bbf7d0; border-color: rgba(74,222,128,0.35); }

/* ---------- Top 3 ---------- */
.top3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.medal {
    text-align: center; padding: 20px 10px; border-radius: 16px;
    background: linear-gradient(160deg, rgba(251,191,36,0.14), rgba(255,255,255,0.03));
    border: 1px solid rgba(251,191,36,0.3);
}
.medal .ic { font-size: 2rem; }
.medal .nm { color: #f8fafc; font-weight: 600; margin-top: 6px; }
.medal .rk { color: #94a3b8; font-size: 0.72rem; letter-spacing: 1px; }

.summary {
    background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(236,72,153,0.12));
    border: 1px solid rgba(129,140,248,0.3); border-radius: 20px; padding: 20px 24px;
    color: #e2e8f0; line-height: 1.7; margin-bottom: 16px;
}
.footer { text-align: center; color: #64748b; font-size: 0.78rem; margin-top: 2.5rem; }

@media (max-width: 640px) {
    .grid, .top3 { grid-template-columns: 1fr; }
    .hero h1 { font-size: 2.1rem; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ---------- helpers ----------
def esc(x):
    return html.escape(str(x))


def tags(items, cls):
    if not items:
        return "<span style='color:#64748b'>Not found</span>"
    return "".join(f'<span class="tag {cls}">{esc(i)}</span>' for i in items)


def glass(title, inner):
    return f'<div class="glass"><div class="sec-title">{title}</div>{inner}</div>'


def load_sample():
    st.session_state["jd_input"] = SAMPLE


# ---------- hero ----------
st.markdown(
    '<div class="hero">'
    '<span class="badge">✨ POWERED BY LANGGRAPH + AI</span>'
    '<h1>AI Job Description Analyzer</h1>'
    '<p>Kisi bhi job description ko ek structured hiring report mein badlein</p>'
    '</div>'
    '<div class="pipeline">'
    '<div class="step"><span class="num">1</span>Extraction</div><span class="arrow">→</span>'
    '<div class="step"><span class="num">2</span>Classification</div><span class="arrow">→</span>'
    '<div class="step"><span class="num">3</span>Skill Analysis</div><span class="arrow">→</span>'
    '<div class="step"><span class="num">4</span>Hiring Report</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---------- input ----------
jd = st.text_area(
    "Job Description",
    key="jd_input",
    height=230,
    placeholder="Yahan job description paste karein...",
)

col1, col2, _ = st.columns([1.2, 1.4, 3])
analyze = col1.button("🚀 Analyze", type="primary")
col2.button("📄 Sample try karein", on_click=load_sample)

if analyze:
    try:
        with st.spinner("AI kaam kar raha hai... 4 nodes chal rahe hain ⚙️"):
            st.session_state["report"] = analyze_job_description(jd)
    except ValueError as e:
        st.session_state.pop("report", None)
        st.warning(str(e))
    except Exception as e:
        st.session_state.pop("report", None)
        st.error(f"Kuch masla aa gaya: {e}")

# ---------- report ----------
report = st.session_state.get("report")
if report:
    st.markdown(
        '<div class="report-head"><h2>📊 Structured Hiring Report</h2>'
        '<span>AI ne job description analyze kar di</span></div>',
        unsafe_allow_html=True,
    )

    overview = (
        '<div class="grid">'
        f'<div class="stat"><div class="k">Job Title</div><div class="v">{esc(report.job_title)}</div></div>'
        f'<div class="stat"><div class="k">Company</div><div class="v">{esc(report.company)}</div></div>'
        f'<div class="stat"><div class="k">Experience</div><div class="v">{esc(report.experience)}</div></div>'
        f'<div class="stat"><div class="k">Category</div><div class="v">{esc(report.job_category)}</div></div>'
        '</div>'
        '<div class="pills">'
        f'<span class="pill">💼 {esc(report.employment_type)}</span>'
        f'<span class="pill pink">📍 {esc(report.work_mode)}</span>'
        '</div>'
    )
    st.markdown(glass("Overview", overview), unsafe_allow_html=True)

    st.markdown(glass("Required Skills", tags(report.required_skills, "req")), unsafe_allow_html=True)
    st.markdown(glass("Technical Skills", tags(report.technical_skills, "tech")), unsafe_allow_html=True)
    st.markdown(glass("Soft Skills", tags(report.soft_skills, "soft")), unsafe_allow_html=True)

    icons = ["🥇", "🥈", "🥉"]
    medals = "".join(
        f'<div class="medal"><div class="ic">{icons[i]}</div>'
        f'<div class="nm">{esc(s)}</div><div class="rk">RANK {i + 1}</div></div>'
        for i, s in enumerate(report.top_3_skills[:3])
    )
    st.markdown(glass("🏆 Top 3 Most Important Skills", f'<div class="top3">{medals}</div>'), unsafe_allow_html=True)

    st.markdown(f'<div class="summary">💡 {esc(report.summary)}</div>', unsafe_allow_html=True)

    st.download_button(
        "⬇️ Download Report (JSON)",
        report_to_json(report),
        file_name="hiring_report.json",
        mime="application/json",
    )

st.markdown('<div class="footer">Built with LangGraph • Pydantic • Streamlit</div>', unsafe_allow_html=True)