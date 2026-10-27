"""CLI: python main.py  (ya)  python main.py job.txt"""
import sys
from core.graph import analyze_job_description
from core.export import save_report_json


def print_report(r):
    print("\n" + "=" * 50 + "\n STRUCTURED HIRING REPORT\n" + "=" * 50)
    print(f"Job Title      : {r.job_title}")
    print(f"Company        : {r.company}")
    print(f"Experience     : {r.experience}")
    print(f"Required Skills: {', '.join(r.required_skills)}")
    print(f"Job Category   : {r.job_category}")
    print(f"Employment Type: {r.employment_type} ({r.work_mode})")
    print(f"Technical      : {', '.join(r.technical_skills)}")
    print(f"Soft Skills    : {', '.join(r.soft_skills)}")
    print("Top 3 Skills   :")
    for i, s in enumerate(r.top_3_skills, 1):
        print(f"  {i}. {s}")
    print(f"\nSummary: {r.summary}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = open(sys.argv[1], encoding="utf-8").read()
    else:
        print("Job description paste karein (khatam karne ke liye empty line + Ctrl+D / Ctrl+Z):")
        text = sys.stdin.read()
    try:
        report = analyze_job_description(text)
        print_report(report)
        print(f"JSON saved: {save_report_json(report)}")
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")
