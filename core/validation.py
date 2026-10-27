"""Input validation - empty / invalid input gracefully handle karta hai."""
MIN_CHARS = 30
MAX_CHARS = 15000


def validate_job_description(text) -> str:
    """Clean text return karta hai, ya ValueError raise karta hai (user-friendly message ke sath)."""
    if text is None or not isinstance(text, str):
        raise ValueError("Job description text honi chahiye.")
    text = text.strip()
    if not text:
        raise ValueError("Job description khali hai. Please job description paste karein.")
    if len(text) < MIN_CHARS:
        raise ValueError(f"Job description bohot chhoti hai (kam az kam {MIN_CHARS} characters chahiye).")
    if len(text) > MAX_CHARS:
        raise ValueError(f"Job description bohot lambi hai (max {MAX_CHARS} characters).")
    if sum(c.isalpha() for c in text) < len(text) * 0.4:
        raise ValueError("Input valid job description nahi lagti. Please sahi text paste karein.")
    return text
