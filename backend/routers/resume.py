from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.user import User, Resume, UserSkill
from services.auth_service import get_current_user
from services.resume_service import save_upload, extract_text, analyze_resume

router = APIRouter()


@router.post("/upload", status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        filename, file_path = await save_upload(file, str(current_user.id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    parsed_text = extract_text(file_path)

    resume = Resume(
        user_id=current_user.id,
        filename=filename,
        file_path=file_path,
        parsed_text=parsed_text,
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    return {"resume_id": str(resume.id), "message": "Resume uploaded. Call /resume/analyze to process it."}


@router.post("/analyze")
async def analyze(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get latest resume
    result = await db.execute(
        select(Resume).where(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).limit(1)
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found. Upload one first.")

    if not resume.parsed_text:
        raise HTTPException(status_code=400, detail="Resume text could not be extracted.")

    analysis = await analyze_resume(
        parsed_text=resume.parsed_text,
        target_company=current_user.target_company or "",
        target_role=current_user.target_role or "",
    )

    resume.extracted_skills = analysis.get("skills", [])
    resume.analysis_result = analysis

    # Auto-update user skills from resume
    for skill_name in analysis.get("skills", []):
        existing = next((s for s in current_user.skills if s.skill_name.lower() == skill_name.lower()), None)
        if not existing:
            db.add(UserSkill(user_id=current_user.id, skill_name=skill_name, proficiency="beginner"))

    return {
        "extracted_skills": analysis.get("skills", []),
        "experience_years": analysis.get("experience_years", 0),
        "education": analysis.get("education", {}),
        "skill_gap": analysis.get("skill_gap", {}),
        "recommendations": analysis.get("recommendations", []),
    }


@router.get("")
async def get_latest_resume(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Resume).where(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).limit(1)
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found")
    return {
        "resume_id": str(resume.id),
        "filename": resume.filename,
        "extracted_skills": resume.extracted_skills,
        "analysis_result": resume.analysis_result,
        "created_at": resume.created_at,
    }
