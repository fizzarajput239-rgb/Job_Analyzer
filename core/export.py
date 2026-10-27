"""Report ko JSON file mein export karna."""
import json
from pathlib import Path
from core.models import HiringReport


def report_to_json(report: HiringReport) -> str:
    return json.dumps(report.model_dump(), indent=2, ensure_ascii=False)


def save_report_json(report: HiringReport, path: str = "hiring_report.json") -> Path:
    p = Path(path)
    p.write_text(report_to_json(report), encoding="utf-8")
    return p
