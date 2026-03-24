from fastapi import APIRouter
from ai.knowledge_base import COMPANIES, get_company_roles, get_company_skills

router = APIRouter()


@router.get("")
async def list_companies():
    return [
        {"name": name, "type": data.get("type", "")}
        for name, data in COMPANIES.items()
    ]


@router.get("/{company}/roles")
async def get_roles(company: str):
    roles = get_company_roles(company)
    if not roles:
        return {"company": company, "roles": []}
    return {"company": company, "roles": roles}


@router.get("/{company}/roles/{role}/skills")
async def get_skills(company: str, role: str):
    skills = get_company_skills(company, role)
    return {"company": company, "role": role, "required_skills": skills}
