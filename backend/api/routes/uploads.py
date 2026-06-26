from fastapi import APIRouter, UploadFile, File, Depends
from backend.services.skill_extraction.extractor import SkillExtractor
from backend.providers.llm.gemini import GeminiAdapter
from backend.providers.storage.supabase_storage import SupabaseStorageAdapter
from backend.core.database import supabase
import uuid, io
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document

router = APIRouter(prefix="/v1/uploads", tags=["uploads"])

def get_llm(): return GeminiAdapter()
def get_storage(): return SupabaseStorageAdapter()

def extract_text_from_file(content: bytes, filename: str) -> str:
    if filename.endswith(".pdf"):
        return pdf_extract_text(io.BytesIO(content))
    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        return "
".join([p.text for p in doc.paragraphs])
    return content.decode("utf-8", errors="ignore")

@router.post("/resume")
async def upload_resume(file: UploadFile = File(...), llm=Depends(get_llm), storage=Depends(get_storage)):
    content = await file.read()
    user_id = str(uuid.uuid4())  # replace with auth user id
    path = await storage.put_resume(user_id, content, file.filename)
    text = extract_text_from_file(content, file.filename)
    extractor = SkillExtractor(llm)
    skills = await extractor.extract(text, "resume")
    # TODO: persist parsed_document to supabase
    return {"path": path, "skills": skills}

@router.post("/job-description")
async def upload_jd(file: UploadFile = File(...), llm=Depends(get_llm), storage=Depends(get_storage)):
    content = await file.read()
    text = extract_text_from_file(content, file.filename or "jd.txt")
    extractor = SkillExtractor(llm)
    skills = await extractor.extract(text, "job_description")
    return {"skills": skills}
