"""4 LangGraph nodes. Har node state leta hai aur state ka update dict return karta hai."""
from core.llm import get_llm
from core.models import ExtractedInfo, JobClassification, SkillAnalysis, HiringReport
from core.state import GraphState


def _structured(schema):
    return get_llm().with_structured_output(schema)


# ---------- Node 1: Information Extraction ----------
def extract_info_node(state: GraphState) -> GraphState:
    if state.get("error"):
        return {}
    try:
        prompt = (
            "Extract the job title, company name (if available), required experience and "
            "required skills from this job description. Do not invent information.\n\n"
            f"JOB DESCRIPTION:\n{state['job_description']}"
        )
        result = _structured(ExtractedInfo).invoke(prompt)
        return {"extracted": result}
    except Exception as e:
        return {"error": f"Node 1 (Extraction) failed: {e}"}


# ---------- Node 2: Job Classification ----------
def classify_job_node(state: GraphState) -> GraphState:
    if state.get("error"):
        return {}
    try:
        info = state["extracted"]
        prompt = (
            "Classify this job into a job category, employment type "
            "(Full-time, Part-time, Internship, Contract) and work mode (Remote, Hybrid, On-site). "
            "Use 'Not specified' if not mentioned.\n\n"
            f"Extracted info: {info.model_dump_json()}\n\n"
            f"JOB DESCRIPTION:\n{state['job_description']}"
        )
        result = _structured(JobClassification).invoke(prompt)
        return {"classification": result}
    except Exception as e:
        return {"error": f"Node 2 (Classification) failed: {e}"}


# ---------- Node 3: Skill Analysis ----------
def analyze_skills_node(state: GraphState) -> GraphState:
    if state.get("error"):
        return {}
    try:
        info = state["extracted"]
        prompt = (
            "Split the skills into technical skills and soft skills (infer common soft skills "
            "only if the text supports them), and pick the 3 MOST important skills for this role.\n\n"
            f"Job title: {info.job_title}\n"
            f"Required skills: {', '.join(info.required_skills)}\n\n"
            f"JOB DESCRIPTION:\n{state['job_description']}"
        )
        result = _structured(SkillAnalysis).invoke(prompt)
        result.top_3_skills = result.top_3_skills[:3]
        return {"skills": result}
    except Exception as e:
        return {"error": f"Node 3 (Skill Analysis) failed: {e}"}


# ---------- Node 4: Hiring Report ----------
def generate_report_node(state: GraphState) -> GraphState:
    if state.get("error"):
        return {}
    try:
        info, cls, sk = state["extracted"], state["classification"], state["skills"]

        summary_prompt = (
            "Write a 2-sentence hiring summary for recruiters based on this data:\n"
            f"{info.model_dump_json()}\n{cls.model_dump_json()}\n{sk.model_dump_json()}"
        )
        try:
            summary = get_llm().invoke(summary_prompt).content
            summary = summary if isinstance(summary, str) else str(summary)
        except Exception:
            summary = f"{info.job_title} role in {cls.job_category}, {cls.employment_type}."

        report = HiringReport(
            job_title=info.job_title,
            company=info.company_name or "Not specified",
            experience=info.required_experience,
            required_skills=info.required_skills,
            job_category=cls.job_category,
            employment_type=cls.employment_type,
            work_mode=cls.work_mode,
            technical_skills=sk.technical_skills,
            soft_skills=sk.soft_skills,
            top_3_skills=sk.top_3_skills,
            summary=summary.strip(),
        )
        return {"report": report}
    except Exception as e:
        return {"error": f"Node 4 (Report) failed: {e}"}
