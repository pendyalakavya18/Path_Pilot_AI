"""
eligibility_service.py — Company eligibility check logic
"""

from ai.knowledge_base import COMPANIES


def check_eligibility(
    company: str,
    user_cgpa: float,
    user_branch: str,
    user_experience: float,
    user_skills: list[str],
) -> dict:
    company_data = COMPANIES.get(company.lower(), COMPANIES.get(company, None))
    if not company_data:
        return {
            "eligible": None,
            "reason": f"Company '{company}' not found in our database.",
            "suggestions": [],
        }

    requirements = company_data.get("requirements", {})
    min_cgpa = requirements.get("min_cgpa", 0.0)
    allowed_branches = requirements.get("branches", [])  # empty = all branches
    min_experience = requirements.get("min_experience", 0.0)
    required_skills = requirements.get("required_skills", [])

    failures = []

    if user_cgpa and user_cgpa < min_cgpa:
        failures.append(f"CGPA {user_cgpa} is below the minimum requirement of {min_cgpa}")

    if allowed_branches and user_branch and user_branch not in allowed_branches:
        failures.append(f"Branch '{user_branch}' is not eligible. Accepted: {', '.join(allowed_branches)}")

    if user_experience < min_experience:
        failures.append(f"Experience {user_experience} years is below minimum {min_experience} years")

    user_skills_lower = {s.lower() for s in user_skills}
    missing = [s for s in required_skills if s.lower() not in user_skills_lower]
    if missing:
        failures.append(f"Missing required skills: {', '.join(missing)}")

    return {
        "company": company,
        "eligible": len(failures) == 0,
        "failures": failures,
        "requirements": requirements,
    }


def get_eligible_companies(
    user_cgpa: float,
    user_branch: str,
    user_experience: float,
    user_skills: list[str],
) -> list[dict]:
    eligible = []
    for company_name in COMPANIES:
        result = check_eligibility(company_name, user_cgpa, user_branch, user_experience, user_skills)
        if result.get("eligible"):
            eligible.append({"company": company_name, "type": COMPANIES[company_name].get("type", "")})
    return eligible
