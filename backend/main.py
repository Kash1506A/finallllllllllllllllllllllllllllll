# backend/main.py - FIXED IMPORTS

import sys
import os
from pathlib import Path

# FIX: Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
from typing import Optional
from datetime import datetime

from backend.ai_brain import AdvancedAIBrain
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
ai_brain = AdvancedAIBrain()
db = ProjectDB()
pipeline = EnhancedVideoPipeline()

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
    """AI analyzes editing request with emotional intelligence"""
    try:
        video_metadata = {
            "duration": 180,
            "resolution": "1920x1080",
            "fps": 30,
            "has_audio": True
        }
        
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

@app.post("/api/analyze/complete")
async def analyze_complete(request: EditRequest):
    """Complete AI analysis with full workflow planning"""
    try:
        video_metadata = {
            "duration": 180,
            "resolution": "1920x1080",
            "fps": 30,
            "has_audio": True
        }
        
        plan = await ai_brain.analyze_request(request.user_prompt, video_metadata)
        
        # Extract key insights
        analysis = plan.get("analysis", {})
        operations = plan.get("operations", [])
        creative_decisions = plan.get("creative_decisions", {})
        
        # Calculate engagement score (0-10)
        engagement_factors = []
        if any(op["name"] == "analyze_emotions" for op in operations):
            engagement_factors.append(2)
        if any(op["name"] == "add_music" for op in operations):
            engagement_factors.append(2)
        if any(op["name"] == "add_subtitles" for op in operations):
            engagement_factors.append(2)
        if any(op["name"] == "color_correction" for op in operations):
            engagement_factors.append(2)
        if any(op["name"] == "identify_key_moments" for op in operations):
            engagement_factors.append(2)
        
        engagement_score = min(10, sum(engagement_factors))
        
        return {
            "success": True,
            "workflow_plan": {
                "analysis": {
                    "emotion": analysis.get("detected_emotion", "balanced"),
                    "content_type": analysis.get("content_type", "general"),
                    "quality_score": 8.5
                },
                "operations": [
                    {
                        **op,
                        "phase": self._get_operation_phase(op["name"]),
                        "estimated_time": self._estimate_operation_time(op["name"])
                    }
                    for op in operations
                ],
                "creative_decisions": creative_decisions
            },
            "key_insights": {
                "detected_emotion": analysis.get("detected_emotion", "balanced"),
                "content_type": analysis.get("content_type", "general"),
                "total_operations": len(operations),
                "engagement_score": engagement_score
            },
            "estimated_time": len(operations) * 30,
            "features_used": {
                "emotion_analysis": any(op["name"] == "analyze_emotions" for op in operations),
                "key_moments": any(op["name"] == "identify_key_moments" for op in operations),
                "platform_optimization": any(op["name"] == "platform_optimize" for op in operations)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _get_operation_phase(operation_name: str) -> str:
    """Map operation to workflow phase"""
    phase_map = {
        "analyze_emotions": "Analysis",
        "identify_key_moments": "Analysis",
        "remove_fillers": "Core Editing",
        "remove_silence": "Core Editing",
        "enhance_audio": "Core Editing",
        "add_subtitles": "Creative Enhancement",
        "add_music": "Creative Enhancement",
        "color_correction": "Creative Enhancement",
        "platform_optimize": "Platform Optimization"
    }
    return phase_map.get(operation_name, "Processing")

def _estimate_operation_time(operation_name: str) -> int:
    """Estimate time for operation in seconds"""
    time_map = {
        "analyze_emotions": 45,
        "identify_key_moments": 30,
        "remove_fillers": 20,
        "remove_silence": 25,
        "enhance_audio": 15,
        "add_subtitles": 40,
        "add_music": 10,
        "color_correction": 30,
        "platform_optimize": 20
    }
    return time_map.get(operation_name, 30)

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

@app.post("/api/upload/multiplatform", response_model=ProjectResponse)
async def upload_multiplatform(
    video: UploadFile = File(...),
    prompt: str = "",
    platforms: str = "youtube,instagram,tiktok",
    reference: Optional[UploadFile] = None,
    music: Optional[UploadFile] = None
):
    """Upload video for multi-platform optimization"""
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
        
        # Parse platforms
        platform_list = [p.strip() for p in platforms.split(",")]
        
        project_id = db.create_project({
            "input_video": video_path,
            "user_prompt": prompt,
            "reference_video": ref_path,
            "background_music": music_path,
            "platforms": platform_list,
            "multiplatform": True,
            "status": "uploaded"
        })
        
        return ProjectResponse(
            project_id=project_id,
            status="uploaded",
            message=f"Video uploaded for {len(platform_list)} platforms - Ready for AI optimization"
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
        
        plan = await ai_brain.analyze_request(project["user_prompt"], video_metadata)
        
        db.update_project(project_id, {
            "status": "processing",
            "ai_analysis": plan.get("analysis", {}),
            "creative_decisions": plan.get("creative_decisions", {})
        })
        
        operations = [
            Operation(
                name=op["name"],
                priority=op.get("priority", 999),
                params=op.get("params", {})
            )
            for op in plan.get("operations", [])
        ]
        
        output_path = f"data/outputs/{project_id}_output.mp4"
        result = pipeline.process(
            input_path=project["input_video"],
            operations=operations,
            output_path=output_path
        )
        
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

@app.post("/api/process/complete/{project_id}", response_model=ProjectResponse)
async def process_video_complete(project_id: str, background_tasks: BackgroundTasks):
    """Start complete processing workflow with all AI features"""
    try:
        project = db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Check if multiplatform
        is_multiplatform = project.get("multiplatform", False)
        platforms = project.get("platforms", ["youtube"])
        
        # Start background processing
        background_tasks.add_task(process_video_background, project_id)
        
        message = "AI Brain analyzing emotions and planning creative edits..."
        if is_multiplatform:
            message = f"Processing for {len(platforms)} platforms: {', '.join(platforms)}"
        
        return ProjectResponse(
            project_id=project_id,
            status="processing",
            message=message
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{project_id}")
async def get_status(project_id: str):
    """Get project status with detailed progress"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
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

@app.get("/api/status/{project_id}/detailed")
async def get_detailed_status(project_id: str):
    """Get detailed project status with full metadata"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    status_messages = {
        "uploaded": "Video uploaded, ready to process",
        "analyzing": "AI Brain analyzing emotions and content...",
        "processing": "Applying creative edits based on AI analysis...",
        "completed": "Video ready! AI-powered edits complete",
        "failed": "Processing failed"
    }
    
    phase_messages = {
        "uploaded": "📥 Phase 1: Video Upload Complete",
        "analyzing": "🧠 Phase 2: AI Emotion Analysis",
        "processing": "⚙️ Phase 3-4: Processing & Platform Optimization",
        "completed": "✅ Phase 5-6: Final Output Ready",
        "failed": "❌ Processing Failed"
    }
    
    # Calculate progress percentage
    progress = 0
    if project["status"] == "uploaded":
        progress = 10
    elif project["status"] == "analyzing":
        progress = 30
    elif project["status"] == "processing":
        progress = 70
    elif project["status"] == "completed":
        progress = 100
    elif project["status"] == "failed":
        progress = 0
    
    # Get metadata
    video_metadata = project.get("video_metadata", {})
    ai_analysis = project.get("ai_analysis", {})
    creative_decisions = project.get("creative_decisions", {})
    
    return {
        **project,
        "status_message": status_messages.get(project["status"], project["status"]),
        "status_description": status_messages.get(project["status"], project["status"]),
        "workflow_diagram_phase": phase_messages.get(project["status"], project["status"]),
        "progress": progress,
        "progress_percentage": progress,
        "details": {
            "emotions_analyzed": len(video_metadata.get("emotions", [])),
            "key_moments_found": len(video_metadata.get("key_moments", [])),
            "quality_score": video_metadata.get("quality_metrics", {}).get("overall_score", 0),
            "ai_features_used": list(ai_analysis.keys()) if ai_analysis else [],
            "platforms": project.get("platforms", ["youtube"]),
            "multiplatform": project.get("multiplatform", False)
        },
        "timestamps": {
            "uploaded_at": project.get("created_at"),
            "completed_at": project.get("completed_at")
        }
    }

@app.get("/api/download/{project_id}")
async def download_video(project_id: str):
    """Download processed video (master version)"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project["status"] != "completed":
        raise HTTPException(status_code=400, detail="Video not ready")
    
    output_path = project.get("output_video")
    if not output_path or not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    # Get file size for logging
    file_size = os.path.getsize(output_path)
    print(f"📥 Downloading: {project_id} ({file_size / (1024*1024):.2f} MB)")
    
    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename=f"{project_id}_edited.mp4",
        headers={
            "Content-Disposition": f'attachment; filename="{project_id}_edited.mp4"',
            "Cache-Control": "no-cache"
        }
    )

@app.get("/api/download/{project_id}/{platform}")
async def download_platform_video(project_id: str, platform: str):
    """Download platform-specific video version"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project["status"] != "completed":
        raise HTTPException(status_code=400, detail="Video not ready")
    
    # Map platform to output file
    platform = platform.lower()
    
    # For now, return the same file (in future, you can generate platform-specific versions)
    output_path = project.get("output_video")
    
    # Check for platform-specific output
    platform_output = project.get(f"output_{platform}")
    if platform_output and os.path.exists(platform_output):
        output_path = platform_output
    
    if not output_path or not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail=f"Video file not found for {platform}")
    
    # Get file size for logging
    file_size = os.path.getsize(output_path)
    print(f"📥 Downloading {platform} version: {project_id} ({file_size / (1024*1024):.2f} MB)")
    
    filename_map = {
        "youtube": f"{project_id}_youtube_16x9.mp4",
        "instagram": f"{project_id}_instagram_9x16.mp4",
        "tiktok": f"{project_id}_tiktok_9x16.mp4",
        "master": f"{project_id}_master.mp4"
    }
    
    filename = filename_map.get(platform, f"{project_id}_{platform}.mp4")
    
    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename=filename,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache"
        }
    )

@app.get("/api/preview/{project_id}")
async def preview_video(project_id: str):
    """Stream video for preview (doesn't trigger download)"""
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
        headers={
            "Accept-Ranges": "bytes",
            "Cache-Control": "no-cache"
        }
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

@app.get("/api/project/{project_id}/files")
async def check_project_files(project_id: str):
    """Check if project files exist"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    files_status = {}
    for key in ["input_video", "output_video", "reference_video", "background_music"]:
        file_path = project.get(key)
        if file_path:
            files_status[key] = {
                "path": file_path,
                "exists": os.path.exists(file_path),
                "size_mb": os.path.getsize(file_path) / (1024*1024) if os.path.exists(file_path) else 0
            }
    
    return {
        "project_id": project_id,
        "status": project["status"],
        "files": files_status
    }

@app.delete("/api/project/{project_id}")
async def delete_project(project_id: str):
    """Delete a project and its files"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Delete files
    deleted_files = []
    for key in ["input_video", "output_video", "reference_video", "background_music"]:
        file_path = project.get(key)
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                deleted_files.append(key)
                print(f"🗑️  Deleted {key}: {file_path}")
            except Exception as e:
                print(f"⚠️  Could not delete {key}: {e}")
    
    # Delete from database
    db.delete_project(project_id)
    
    return {
        "message": "Project deleted successfully",
        "deleted_files": deleted_files
    }

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