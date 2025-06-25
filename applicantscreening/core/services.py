
from .models import Applicant, ScreeningCriteria



def passes_screening(applicant: "Applicant", criteria: "ScreeningCriteria") -> bool:
    if criteria.min_experience and (applicant.experience or 0) < criteria.min_experience:
        return False
    if criteria.min_qualification and criteria.min_qualification.lower() not in (applicant.education or "").lower():
        return False
    if criteria.required_skills:
        req = {s.strip().lower() for s in criteria.required_skills.split(",")}
        hav = {s.strip().lower() for s in (applicant.skills or "").split(",")}
        if not req.issubset(hav): return False
    return True
