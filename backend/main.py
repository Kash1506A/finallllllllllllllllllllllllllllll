# backend/main.py - FIXED FOR PROMPT-ONLY MODE

import sys
import os
from pathlib import Path

# FIX: Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Form
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
    title="NeuralFlare AI Video Editor - Prompt-Only Mode",
    description="AI-powered video editing - executes only what you request",
    version="2.0-PromptOnly"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
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
        "message": "NeuralFlare AI Video Editor API - Prompt-Only Mode",
        "version": "2.0-PromptOnly",
        "status": "operational",
        "mode": "PROMPT-ONLY",
        "features": [
            "Execute only user-specified operations",
            "No automatic operations",
            "Smart prompt detection",
            "Multi-Platform Optimization"
        ],
        "examples": [
            "remove noise and add subtitles",
            "enhance audio and remove silence",
            "add music and optimize for instagram",
            "remove fillers and add captions"
        ]
    }

@app.post("/api/analyze")
async def analyze_request(request: EditRequest):
    """AI analyzes editing request - PROMPT-ONLY MODE"""
    try:
        # Check for empty prompt
        if not request.user_prompt or len(request.user_prompt.strip()) < 3:
            return {
                "success": False,
                "error": "Empty prompt",
                "message": "Please specify what you want to do. Examples: 'remove noise and add subtitles', 'enhance audio', 'add music for instagram'",
                "plan": {
                    "analysis": {"mode": "error"},
                    "operations": []
                }
            }
        
        video_metadata = {
            "duration": 180,
            "resolution": "1920x1080",
            "fps": 30,
            "has_audio": True
        }
        
        # Get AI plan based on prompt ONLY
        plan = await ai_brain.analyze_request(request.user_prompt, video_metadata)
        
        # Check if operations were detected
        operations = plan.get("operations", [])
        if not operations:
            return {
                "success": False,
                "error": "No operations detected",
                "message": f"Could not understand your request: '{request.user_prompt}'. Please be more specific. Examples: 'remove background noise', 'add subtitles', 'enhance audio and remove silence'",
                "plan": plan
            }
        
        return {
            "success": True,
            "plan": plan,
            "estimated_time": len(operations) * 30,
            "operations_count": len(operations),
            "operations_list": [op["name"].replace("_", " ").title() for op in operations]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/complete")
async def analyze_complete(request: EditRequest):
    """Complete AI analysis - PROMPT-ONLY MODE"""
    try:
        # Check for empty prompt
        if not request.user_prompt or len(request.user_prompt.strip()) < 3:
            return {
                "success": False,
                "error": "Empty prompt",
                "message": "Please describe what edits you want"
            }
        
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
        
        # Check if operations were detected
        if not operations:
            return {
                "success": False,
                "error": "No operations detected",
                "message": f"Could not detect any operations from: '{request.user_prompt}'"
            }
        
        # Calculate engagement score
        engagement_score = min(10, len(operations) * 2)
        
        return {
            "success": True,
            "workflow_plan": {
                "analysis": analysis,
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
                "mode": "prompt-only",
                "detected_emotion": analysis.get("detected_emotion", "none"),
                "platform": analysis.get("platform", "youtube"),
                "total_operations": len(operations),
                "engagement_score": engagement_score
            },
            "estimated_time": len(operations) * 30,
            "operations_list": [op["name"].replace("_", " ").title() for op in operations]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

def _get_operation_phase(operation_name: str) -> str:
    """Map operation to workflow phase"""
    phase_map = {
        "analyze_emotions": "Analysis",
        "identify_key_moments": "Analysis",
        "remove_fillers": "Core Editing",
        "remove_silence": "Core Editing",
        "enhance_audio": "Audio Enhancement",
        "remove_background_noise": "Audio Enhancement",
        "isolate_voice": "Audio Enhancement",
        "add_subtitles": "Creative Enhancement",
        "add_music": "Creative Enhancement",
        "color_correction": "Visual Enhancement",
        "brightness_adjustment": "Visual Enhancement",
        "platform_optimize": "Platform Optimization",
        "detect_bad_words": "Content Moderation"
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
        "remove_background_noise": 20,
        "isolate_voice": 25,
        "add_subtitles": 40,
        "add_music": 10,
        "color_correction": 30,
        "brightness_adjustment": 15,
        "platform_optimize": 20,
        "detect_bad_words": 30
    }
    return time_map.get(operation_name, 30)

@app.post("/api/upload", response_model=ProjectResponse)
async def upload_video(
    video: UploadFile = File(...),
    prompt: str = Form(""),
    reference: Optional[UploadFile] = File(None),
    music: Optional[UploadFile] = File(None)
):
    """Upload video and create project"""
    try:
        # Validate prompt
        if not prompt or len(prompt.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Prompt is required. Please specify what edits you want (e.g., 'remove noise and add subtitles')"
            )
        
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
            message=f"Video uploaded - Will execute: {prompt}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload/multiplatform", response_model=ProjectResponse)
async def upload_multiplatform(
    video: UploadFile = File(...),
    prompt: str = Form(""),
    platforms: str = Form("youtube,instagram,tiktok"),
    reference: Optional[UploadFile] = File(None),
    music: Optional[UploadFile] = File(None)
):
    """Upload video for multi-platform optimization"""
    try:
        # Validate prompt
        if not prompt or len(prompt.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Prompt is required. Please specify what edits you want (e.g., 'remove noise and add subtitles')"
            )
        
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
            message=f"Video uploaded for {len(platform_list)} platforms - Will execute: {prompt}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

async def process_video_background(project_id: str):
    """Background task to process video - PROMPT-ONLY MODE"""
    try:
        project = db.get_project(project_id)
        if not project:
            print(f"❌ Project not found: {project_id}")
            return
        
        # Check for valid prompt
        user_prompt = project.get("user_prompt", "").strip()
        if not user_prompt or len(user_prompt) < 3:
            print(f"❌ Empty prompt for project: {project_id}")
            db.update_project(project_id, {
                "status": "failed",
                "error": "Empty prompt - no operations specified"
            })
            return
        
        print(f"\n{'='*70}")
        print(f"🎬 PROCESSING PROJECT: {project_id}")
        print(f"📝 User Prompt: '{user_prompt}'")
        print(f"{'='*70}\n")
        
        db.update_project(project_id, {"status": "analyzing"})
        
        # Get video metadata
        from moviepy.editor import VideoFileClip
        try:
            print("📹 Loading video metadata...")
            temp_video = VideoFileClip(project["input_video"])
            video_metadata = {
                "duration": temp_video.duration,
                "resolution": f"{temp_video.w}x{temp_video.h}",
                "fps": temp_video.fps,
                "has_audio": temp_video.audio is not None
            }
            temp_video.close()
            print(f"✅ Video: {video_metadata['duration']:.1f}s, {video_metadata['resolution']}, {video_metadata['fps']}fps")
        except Exception as e:
            print(f"⚠️ Could not read video metadata: {e}")
            video_metadata = {"duration": 120, "resolution": "1920x1080", "fps": 30, "has_audio": True}
        
        # Get AI plan from prompt ONLY
        print("\n🧠 AI BRAIN: Analyzing prompt...")
        plan = await ai_brain.analyze_request(user_prompt, video_metadata)
        
        # Check if operations were detected
        operations_data = plan.get("operations", [])
        if not operations_data or len(operations_data) == 0:
            print(f"❌ No operations detected from prompt: '{user_prompt}'")
            db.update_project(project_id, {
                "status": "failed",
                "error": f"No operations detected from prompt: '{user_prompt}'. Please be more specific."
            })
            return
        
        print(f"✅ Detected {len(operations_data)} operations:")
        for op in operations_data:
            print(f"   - {op['name'].replace('_', ' ').title()}")
        
        db.update_project(project_id, {
            "status": "processing",
            "ai_analysis": plan.get("analysis", {}),
            "creative_decisions": plan.get("creative_decisions", {}),
            "operations_detected": len(operations_data)
        })
        
        # Convert to Operation objects
        print(f"\n⚙️ Creating operation pipeline...")
        operations = []
        for op in operations_data:
            operation = Operation(
                name=op["name"],
                priority=op.get("priority", 999),
                params=op.get("params", {})
            )
            operations.append(operation)
            print(f"   ✓ Added: {operation.name} (priority: {operation.priority})")
        
        print(f"\n🎬 Starting video pipeline with {len(operations)} operations...\n")
        
        # Process video
        output_path = f"data/outputs/{project_id}_output.mp4"
        
        try:
            result = pipeline.process(
                input_path=project["input_video"],
                operations=operations,
                output_path=output_path
            )
            
            print(f"\n✅ PROCESSING COMPLETE!")
            print(f"📂 Output saved: {output_path}")
            
            # Check if file was created
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f"📊 File size: {file_size:.2f} MB")
                
                db.update_project(project_id, {
                    "status": "completed",
                    "output_video": result["output_path"],
                    "editing_plan": plan,
                    "video_metadata": result["metadata"],
                    "completed_at": datetime.now().isoformat(),
                    "output_file_size_mb": file_size
                })
                print(f"✅ Database updated: Status = completed")
            else:
                print(f"❌ Output file not created: {output_path}")
                db.update_project(project_id, {
                    "status": "failed",
                    "error": "Output file was not created"
                })
        
        except Exception as e:
            print(f"\n❌ PIPELINE ERROR: {e}")
            import traceback
            traceback.print_exc()
            db.update_project(project_id, {
                "status": "failed",
                "error": f"Pipeline error: {str(e)}"
            })
    
    except Exception as e:
        print(f"\n❌ BACKGROUND PROCESSING ERROR: {e}")
        import traceback
        traceback.print_exc()
        db.update_project(project_id, {
            "status": "failed",
            "error": str(e)
        })

@app.post("/api/process/{project_id}", response_model=ProjectResponse)
async def process_video(project_id: str, background_tasks: BackgroundTasks):
    """Start processing - PROMPT-ONLY MODE"""
    try:
        project = db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Validate prompt
        user_prompt = project.get("user_prompt", "").strip()
        if not user_prompt or len(user_prompt) < 3:
            raise HTTPException(
                status_code=400,
                detail="No prompt specified. Cannot process without instructions."
            )
        
        background_tasks.add_task(process_video_background, project_id)
        
        return ProjectResponse(
            project_id=project_id,
            status="processing",
            message=f"Processing based on your request: {user_prompt}"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process/complete/{project_id}", response_model=ProjectResponse)
async def process_video_complete(project_id: str, background_tasks: BackgroundTasks):
    """Start complete processing workflow - PROMPT-ONLY MODE"""
    try:
        project = db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Validate prompt
        user_prompt = project.get("user_prompt", "").strip()
        if not user_prompt or len(user_prompt) < 3:
            raise HTTPException(
                status_code=400,
                detail="No prompt specified. Cannot process without instructions."
            )
        
        # Check if multiplatform
        is_multiplatform = project.get("multiplatform", False)
        platforms = project.get("platforms", ["youtube"])
        
        # Start background processing
        background_tasks.add_task(process_video_background, project_id)
        
        message = f"Processing based on your request: {user_prompt}"
        if is_multiplatform:
            message = f"Processing for {len(platforms)} platforms: {', '.join(platforms)} - {user_prompt}"
        
        return ProjectResponse(
            project_id=project_id,
            status="processing",
            message=message
        )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{project_id}")
async def get_status(project_id: str):
    """Get project status"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    status_messages = {
        "uploaded": f"Ready to process: {project.get('user_prompt', 'No prompt')}",
        "analyzing": "Analyzing your request...",
        "processing": "Applying requested edits...",
        "completed": "Processing complete!",
        "failed": f"Failed: {project.get('error', 'Unknown error')}"
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
        "uploaded": f"Ready to process: {project.get('user_prompt', 'No prompt')}",
        "analyzing": "Analyzing your request...",
        "processing": "Applying requested edits...",
        "completed": "Processing complete!",
        "failed": f"Failed: {project.get('error', 'Unknown error')}"
    }
    
    phase_messages = {
        "uploaded": "📥 Phase 1: Video Upload Complete",
        "analyzing": "🧠 Phase 2: Analyzing Request",
        "processing": "⚙️ Phase 3-4: Processing Operations",
        "completed": "✅ Phase 5-6: Complete",
        "failed": "❌ Processing Failed"
    }
    
    # Calculate progress
    progress = 0
    if project["status"] == "uploaded":
        progress = 10
    elif project["status"] == "analyzing":
        progress = 30
    elif project["status"] == "processing":
        progress = 70
    elif project["status"] == "completed":
        progress = 100
    
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
        filename=f"{project_id}_edited.mp4"
    )

@app.get("/api/download/{project_id}/{platform}")
async def download_platform_video(project_id: str, platform: str):
    """Download platform-specific video version"""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project["status"] != "completed":
        raise HTTPException(status_code=400, detail="Video not ready")
    
    platform = platform.lower()
    output_path = project.get("output_video")
    
    platform_output = project.get(f"output_{platform}")
    if platform_output and os.path.exists(platform_output):
        output_path = platform_output
    
    if not output_path or not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail=f"Video file not found for {platform}")
    
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
        filename=filename
    )

@app.get("/api/preview/{project_id}")
async def preview_video(project_id: str):
    """Stream video for preview"""
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
    
    deleted_files = []
    for key in ["input_video", "output_video", "reference_video", "background_music"]:
        file_path = project.get(key)
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                deleted_files.append(key)
                print(f"🗑️ Deleted {key}: {file_path}")
            except Exception as e:
                print(f"⚠️ Could not delete {key}: {e}")
    
    db.delete_project(project_id)
    
    return {
        "message": "Project deleted successfully",
        "deleted_files": deleted_files
    }

@app.get("/api/features")
async def list_features():
    """List all available features"""
    return {
        "mode": "prompt-only",
        "description": "Only executes operations specified in your prompt",
        "available_operations": {
            "audio": ["remove_background_noise", "enhance_audio", "isolate_voice"],
            "editing": ["remove_silence", "remove_fillers", "trim_by_emotion"],
            "visual": ["brightness_adjustment", "color_correction", "stabilization"],
            "creative": ["add_subtitles", "add_music", "add_filters"],
            "moderation": ["detect_bad_words"],
            "optimization": ["platform_optimize", "aspect_ratio", "compression"]
        },
        "example_prompts": [
            "remove noise and add subtitles",
            "enhance audio and remove silence",
            "add music and optimize for instagram",
            "remove fillers and add captions",
            "brighten video and add music"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mode": "PROMPT-ONLY",
        "message": "Only executes operations specified in user prompt",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)