from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
import os

# ================= LOAD ENV =================
load_dotenv()

# ================= IMPORT MODULES =================
from ai_brain import AIBrain
from database import ProjectDB

# ================= LIFESPAN =================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "=" * 50)
    print("🚀 NeuralFlare AI Video Editor Starting...")
    print("=" * 50)

    # Check HuggingFace API Key
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if api_key and api_key.startswith("hf_"):
        print("✅ HuggingFace API key detected")
        print(f"🔑 Key: {api_key[:10]}...{api_key[-5:]}")
    else:
        print("⚠️  No valid HuggingFace API key found")
        print("💡 Add HUGGINGFACE_API_KEY to .env file")

    # Create directories
    for directory in ["data/uploads", "data/outputs", "data/temp"]:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Ready: {directory}")

    print("=" * 50)
    print("✅ Server ready!")
    print("📡 http://localhost:8000")
    print("📚 http://localhost:8000/docs")
    print("=" * 50 + "\n")

    yield  # ---- APP RUNS HERE ----

    print("🛑 NeuralFlare AI Video Editor shutting down...")

# ================= FASTAPI APP =================
app = FastAPI(
    title="NeuralFlare AI Video Editor",
    version="2.0",
    lifespan=lifespan
)

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= GLOBAL INSTANCES =================
ai_brain = AIBrain()
db = ProjectDB()

# ================= MODELS =================
class EditRequest(BaseModel):
    user_prompt: str
    speed_override: float = 1.0
    platform: str = "youtube"
    use_reference: bool = False

class ProjectResponse(BaseModel):
    project_id: str
    status: str
    message: str

# ================= ROUTES =================
@app.get("/")
async def root():
    return {
        "message": "NeuralFlare AI Video Editor API",
        "ai_provider": "HuggingFace (FREE)",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    return {
        "status": "healthy",
        "ai_brain": "active",
        "api_key_configured": bool(api_key and api_key.startswith("hf_")),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/analyze")
async def analyze_editing_request(request: EditRequest):
    try:
        video_metadata = {
            "duration": 180,
            "resolution": "1920x1080",
            "fps": 30,
            "has_audio": True
        }

        plan = await ai_brain.analyze_request(
            request.user_prompt,
            video_metadata
        )

        return {
            "success": True,
            "plan": plan,
            "estimated_time": len(plan.get("operations", [])) * 30
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload", response_model=ProjectResponse)
async def upload_and_create_project(
    video: UploadFile = File(...),
    prompt: str = "",
    reference: Optional[UploadFile] = None,
    music: Optional[UploadFile] = None
):
    try:
        upload_dir = "data/uploads"
        os.makedirs(upload_dir, exist_ok=True)

        video_path = f"{upload_dir}/{video.filename}"
        with open(video_path, "wb") as f:
            f.write(await video.read())

        reference_path = None
        if reference:
            reference_path = f"{upload_dir}/{reference.filename}"
            with open(reference_path, "wb") as f:
                f.write(await reference.read())

        music_path = None
        if music:
            music_path = f"{upload_dir}/{music.filename}"
            with open(music_path, "wb") as f:
                f.write(await music.read())

        project_id = db.create_project({
            "input_video": video_path,
            "user_prompt": prompt,
            "reference_video": reference_path,
            "background_music": music_path,
            "status": "uploaded"
        })

        return ProjectResponse(
            project_id=project_id,
            status="uploaded",
            message="Video uploaded successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process/{project_id}", response_model=ProjectResponse)
async def process_video_project(project_id: str):
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.update_project(project_id, {"status": "processing"})

    video_metadata = {
        "duration": 120,
        "resolution": "1920x1080",
        "fps": 30,
        "has_audio": True
    }

    plan = await ai_brain.analyze_request(
        project.get("user_prompt", "Edit this video"),
        video_metadata
    )

    db.update_project(project_id, {
        "editing_plan": plan,
        "status": "processing"
    })

    return ProjectResponse(
        project_id=project_id,
        status="processing",
        message=f"Processing started with {len(plan.get('operations', []))} steps"
    )

@app.get("/api/status/{project_id}")
async def get_project_status(project_id: str):
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.get("/api/projects")
async def list_all_projects():
    projects = db.get_all_projects()
    return {"projects": projects, "count": len(projects)}

@app.delete("/api/project/{project_id}")
async def delete_project(project_id: str):
    if not db.get_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete_project(project_id)
    return {"message": "Project deleted successfully"}
