"""
resume_service.py — PDF parsing, skill extraction, resume analysis
"""

import os
import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile

from config import settings
from ai.llm_engine import llm_engine


async def save_upload(file: UploadFile, user_id: str) -> tuple[str, str]:
    """Save uploaded file and return (filename, file_path)."""
    ext = Path(file.filename).suffix.lower()
    if ext not in {".pdf", ".docx", ".doc"}:
        raise ValueError("Only PDF and DOCX files are supported")

    safe_name = f"{user_id}_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_name)

    async with aiofiles.open(file_path, "wb") as out:
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValueError(f"File exceeds {settings.MAX_FILE_SIZE_MB}MB limit")
        await out.write(content)

    return safe_name, file_path


def extract_text_from_pdf(file_path: str) -> str:
    """Extract plain text from PDF using PyMuPDF."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception:
        return ""


def extract_text_from_docx(file_path: str) -> str:
    """Extract plain text from DOCX."""
    try:
        from docx import Document
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception:
        return ""


def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith((".docx", ".doc")):
        return extract_text_from_docx(file_path)
    return ""


async def analyze_resume(parsed_text: str, target_company: str = "", target_role: str = "") -> dict:
    """Use LLM to extract skills and generate gap analysis from resume text."""
    return await llm_engine.analyze_resume(
        resume_text=parsed_text,
        target_company=target_company,
        target_role=target_role,
    )
