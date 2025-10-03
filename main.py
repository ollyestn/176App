from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from datetime import datetime
import uuid

# Import our modules
from doc_compare import DocCompare
from meeting_transcribe import MeetingTranscribe

app = FastAPI()

# Create directories if they don't exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize our services
doc_compare_service = DocCompare()
meeting_service = MeetingTranscribe()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Check if user is logged in (this would typically come from session)
    user_logged_in = False  # Placeholder for actual auth check
    username = "User" if user_logged_in else None
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_logged_in": user_logged_in,
        "username": username
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/docchk", response_class=HTMLResponse)
async def doc_compare_page(request: Request):
    # Get history records for current user
    history_records = doc_compare_service.get_history()  # Placeholder
    
    return templates.TemplateResponse("doc_compare.html", {
        "request": request,
        "history_records": history_records
    })

@app.post("/docchk/compare")
async def compare_documents(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    # Generate unique IDs for this comparison
    comparison_id = str(uuid.uuid4())
    
    # Save uploaded files
    file1_path = f"uploads/{comparison_id}_{file1.filename}"
    file2_path = f"uploads/{comparison_id}_{file2.filename}"
    
    with open(file1_path, "wb") as buffer:
        buffer.write(await file1.read())
        
    with open(file2_path, "wb") as buffer:
        buffer.write(await file2.read())
    
    # Perform document comparison
    result_path = f"results/{comparison_id}_result.xlsx"
    success = doc_compare_service.compare(file1_path, file2_path, result_path)
    
    if success:
        # Save record to database
        doc_compare_service.save_record(comparison_id, file1_path, file2_path, result_path)
        return {"success": True, "download_url": f"/download/{comparison_id}"}
    else:
        return {"success": False, "error": "Comparison failed"}

@app.get("/download/{comparison_id}")
async def download_result(comparison_id: str):
    result_path = f"results/{comparison_id}_result.xlsx"
    if os.path.exists(result_path):
        return FileResponse(result_path, filename=f"comparison_{comparison_id}.xlsx")
    else:
        return {"error": "File not found"}

@app.get("/meeting", response_class=HTMLResponse)
async def meeting_page(request: Request):
    # Get history records for current user
    history_records = meeting_service.get_history()  # Placeholder
    
    return templates.TemplateResponse("meeting.html", {
        "request": request,
        "history_records": history_records
    })

@app.post("/meeting/transcribe")
async def transcribe_meeting(
    audio_file: UploadFile = File(None),
    video_file: UploadFile = File(None)
):
    # Generate unique ID for this transcription
    transcription_id = str(uuid.uuid4())
    
    # Save uploaded files
    audio_path = None
    video_path = None
    
    if audio_file:
        audio_path = f"uploads/{transcription_id}_{audio_file.filename}"
        with open(audio_path, "wb") as buffer:
            buffer.write(await audio_file.read())
            
    if video_file:
        video_path = f"uploads/{transcription_id}_{video_file.filename}"
        with open(video_path, "wb") as buffer:
            buffer.write(await video_file.read())
    
    # Perform transcription and processing
    raw_text_path = f"results/{transcription_id}_raw.docx"
    processed_text_path = f"results/{transcription_id}_processed.docx"
    
    success = meeting_service.transcribe_and_process(
        audio_path, video_path, raw_text_path, processed_text_path
    )
    
    if success:
        # Save record to database
        meeting_service.save_record(transcription_id, audio_path, video_path, raw_text_path, processed_text_path)
        return {
            "success": True,
            "raw_download_url": f"/download/raw/{transcription_id}",
            "processed_download_url": f"/download/processed/{transcription_id}"
        }
    else:
        return {"success": False, "error": "Transcription failed"}

@app.get("/download/raw/{transcription_id}")
async def download_raw_text(transcription_id: str):
    file_path = f"results/{transcription_id}_raw.docx"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=f"raw_transcript_{transcription_id}.docx")
    else:
        return {"error": "File not found"}

@app.get("/download/processed/{transcription_id}")
async def download_processed_text(transcription_id: str):
    file_path = f"results/{transcription_id}_processed.docx"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=f"processed_transcript_{transcription_id}.docx")
    else:
        return {"error": "File not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)