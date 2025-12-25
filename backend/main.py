# backend/main.py - UPDATED WITH ENHANCED AI

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import shutil
from typing import Optional
from datetime import datetime

from backend.ai_brain import AdvancedAIBrain  # Use enhanced version
from backend.database import ProjectDB
from backend.models import EditRequest, ProjectResponse
from core.video_pipeline import EnhancedVideoPipeline, Operation

app = FastAPI(
    title="NeuralFlare AI Video Editor - Enhanced",
    description="AI-powered video editing with emotion analysis and creative intelligence",
    version="2.0-Advanced"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ENHANCED components
ai_brain = AdvancedAIBrain()  # Enhanced AI with emotion intelligence
db = ProjectDB()
pipeline = EnhancedVideoPipeline()  # Enhanced pipeline

# Ensure directories exist
os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/outputs", exist_ok=True)
os.makedirs("data/temp", exist_ok=True)
os.makedirs("assets/music", exist_ok=True)

@app.get("/")
async def root():
    return {
        "message": "NeuralFlare AI Video Editor API - Enhanced Edition",
        "version": "2.0-Advanced",
        "status": "operational",
        "features": [
            "Emotional Intelligence Analysis",
            "Creative Decision Engine",
            "Narrative Restructuring",
            "Multi-Platform Optimization",
            "AI Director + Coach"
        ],
        "ai_brain": "advanced"
    }

@app.post("/api/analyze")
async def analyze_request(request: EditRequest):
    """
    AI analyzes editing request with emotional intelligence
    Returns detailed plan with creative decisions
    """
    try:
        video_metadata = {
            "duration": 180,
            "resolution": "1920x1080",
            "fps": 30,
            "has_audio": True
        }
        
        # Get AI plan with analysis
        plan = await ai_brain.analyze_request(request.user_prompt, video_metadata)
        
        return {
            "success": True,
            "plan": plan,
            "estimated_time": len(plan.get("operations", [])) * 30,
            "features_used": [
                "Emotion Analysis" if any(op["name"] == "analyze_emotions" for op in plan.get("operations", [])) else None,
                "Key Moment Detection" if any(op["name"] == "identify_key_moments" for op in plan.get("operations", [])) else None,
                "Platform Optimization" if any(op["name"] == "platform_optimize" for op in plan.get("operations", [])) else None
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload", response_model=ProjectResponse)
async def upload_video(
    video: UploadFile = File(...),
    prompt: str = "",
    reference: Optional[UploadFile] = None,
    music: Optional[UploadFile] = None
):
    """Upload video and create project"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"{timestamp}_{video.filename}"
        video_path = f"data/uploads/{video_filename}"
        
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        ref_path = None
        if reference:
            ref_filename = f"{timestamp}_ref_{reference.filename}"
            ref_path = f"data/uploads/{ref_filename}"
            with open(ref_path, "wb") as buffer:
                shutil.copyfileobj(reference.file, buffer)
        
        music_path = None
        if music:
            music_filename = f"{timestamp}_music_{music.filename}"
            music_path = f"data/uploads/{music_filename}"
            with open(music_path, "wb") as buffer:
                shutil.copyfileobj(music.file, buffer)
        
        project_id = db.create_project({
            "input_video": video_path,
            "user_prompt": prompt,
            "reference_video": ref_path,
            "background_music": music_path,
            "status": "uploaded"
        })
        
        return ProjectResponse(
            project_id=project_id,
            status="uploaded",
            message="Video uploaded successfully - Ready for AI analysis"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_video_background(project_id: str):
    """Background task to process video with enhanced AI"""
    try:
        project = db.get_project(project_id)
        if not project:
            return
        
        db.update_project(project_id, {"status": "analyzing"})
        
        # Get enhanced video metadata
        from moviepy.editor import VideoFileClip
        try:
            temp_video = VideoFileClip(project["input_video"])
            video_metadata = {
                "duration": temp_video.duration,
                "resolution": f"{temp_video.w}x{temp_video.h}",
                "fps": temp_video.fps,
                "has_audio": temp_video.audio is not None
            }
            temp_video.close()
        except:
            video_metadata = {"duration": 120, "resolution": "1920x1080", "fps": 30}
        
        # Get AI plan with emotion intelligence
        plan = await ai_brain.analyze_request(project["user_prompt"], video_metadata)
        
        db.update_project(project_id, {
            "status": "processing",
            "ai_analysis": plan.get("analysis", {}),
            "creative_decisions": plan.get("creative_decisions", {})
        })
        
        # Convert to operations
        operations = [
            Operation(
                name=op["name"],
                priority=op.get("priority", 999),
                params=op.get("params", {})
            )
            for op in plan.get("operations", [])
        ]
        
        # Process video with enhanced pipeline
        output_path = f"data/outputs/{project_id}_output.mp4"
        result = pipeline.process(
            input_path=project["input_video"],
            operations=operations,
            output_path=output_path
        )
        
        # Update project with results and metadata
        db.update_project(project_id, {
            "status": "completed",
            "output_video": result["output_path"],
            "editing_plan": plan,
            "video_metadata": result["metadata"],
            "completed_at": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Processing error: {e}")
        db.update_project(project_id, {
            "status": "failed",
            "error": str(e)
        })

@app.post("/api/process/{project_id}", response_model=ProjectResponse)
async def process_video(project_id: str, background_tasks: BackgroundTasks):
    """Start processing with enhanced AI"""
    try:
        project = db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        background_tasks.add_task(process_video_background, project_id)
        
        return ProjectResponse(
            project_id=project_id,
            status="processing",
            message="AI Brain analyzing emotions and planning creative edits..."
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{project_id}")
async def get_status(project_id: str):
    """Get project status with detailed progress"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Add helpful status messages
    status_messages = {
        "uploaded": "Video uploaded, ready to process",
        "analyzing": "AI Brain analyzing emotions and content...",
        "processing": "Applying creative edits based on AI analysis...",
        "completed": "Video ready! AI-powered edits complete",
        "failed": "Processing failed"
    }
    
    return {
        **project,
        "status_message": status_messages.get(project["status"], project["status"])
    }

@app.get("/api/download/{project_id}")
async def download_video(project_id: str):
    """Download processed video"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project["status"] != "completed":
        raise HTTPException(status_code=400, detail="Video not ready")
    
    output_path = project.get("output_video")
    if not output_path or not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename=f"{project_id}_AI_edited.mp4"
    )

@app.get("/api/metadata/{project_id}")
async def get_metadata(project_id: str):
    """Get AI analysis metadata for project"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "project_id": project_id,
        "ai_analysis": project.get("ai_analysis", {}),
        "creative_decisions": project.get("creative_decisions", {}),
        "video_metadata": project.get("video_metadata", {}),
        "editing_plan": project.get("editing_plan", {})
    }

@app.get("/api/projects")
async def list_projects():
    """List all projects"""
    return {"projects": db.get_all_projects()}

@app.delete("/api/project/{project_id}")
async def delete_project(project_id: str):
    """Delete a project"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key in ["input_video", "output_video", "reference_video", "background_music"]:
        file_path = project.get(key)
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
    
    db.delete_project(project_id)
    return {"message": "Project deleted successfully"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_brain": "advanced",
        "features": {
            "emotion_analysis": True,
            "creative_decisions": True,
            "platform_optimization": True,
            "narrative_restructuring": True
        },
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/features")
async def list_features():
    """List all available AI features"""
    return {
        "emotional_intelligence": {
            "description": "Analyzes facial expressions, voice tone, and energy",
            "operations": ["analyze_emotions", "identify_key_moments"]
        },
        "creative_decisions": {
            "description": "AI selects editing styles, music, pacing",
            "operations": ["add_music", "color_correction", "add_subtitles"]
        },
        "narrative_restructuring": {
            "description": "Reorganizes footage into story arcs",
            "operations": ["identify_key_moments", "remove_silence"]
        },
        "multi_platform": {
            "description": "Optimizes for YouTube, Instagram, TikTok",
            "operations": ["platform_optimize"],
            "platforms": ["youtube (16:9)", "instagram (9:16)", "tiktok (9:16)"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)