# frontend/streamlit_app.py - ENHANCED PROFESSIONAL UI

import streamlit as st
import requests
import time
import json
from datetime import datetime

st.set_page_config(
    page_title="NeuralFlare AI Editor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .stat-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .phase-indicator {
        background: #e0e7ff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.5rem 0;
        font-weight: bold;
        color: #4c51bf;
    }
    
    .success-box {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .platform-badge {
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.9rem;
        margin: 0.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000"

# Session state
if "project_id" not in st.session_state:
    st.session_state.project_id = None
if "workflow_plan" not in st.session_state:
    st.session_state.workflow_plan = None

# Header
st.markdown('<h1 class="main-header">🎬 NeuralFlare AI Video Editor</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">One Input → AI Analysis → Three Platform-Optimized Outputs</p>', unsafe_allow_html=True)

# Sidebar - Workflow Status
with st.sidebar:
    st.markdown("### 🎯 Workflow Phases")
    
    phases = [
        "📥 Raw Video Input",
        "🧠 Emotion Analysis",
        "🎨 Creative Decisions",
        "⚙️ Processing Pipeline",
        "📱 Platform Adaptation",
        "✅ Final Output"
    ]
    
    for i, phase in enumerate(phases, 1):
        st.markdown(f"**{i}.** {phase}")
    
    st.markdown("---")
    st.markdown("### 📊 Features")
    st.markdown("✓ Emotion-Aware Editing")
    st.markdown("✓ AI Creative Engine")
    st.markdown("✓ Multi-Platform Output")
    st.markdown("✓ Auto Story Structure")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🎬 New Project",
    "📊 AI Analysis",
    "📁 My Projects", 
    "ℹ️ About"
])

# ==================== TAB 1: NEW PROJECT ====================
with tab1:
    st.markdown("## Upload & Configure")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📹 Video Upload")
        uploaded_file = st.file_uploader(
            "Select your video",
            type=["mp4", "mov", "avi"],
            help="Supported formats: MP4, MOV, AVI"
        )
        
        if uploaded_file:
            st.success(f"✅ Video loaded: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.1f} MB)")
        
        st.markdown("### 🎵 Background Music (Optional)")
        music_file = st.file_uploader(
            "Add custom music",
            type=["mp3", "wav"],
            help="Or let AI choose music based on mood"
        )
        
        st.markdown("### 💬 Tell AI What You Want")
        prompt = st.text_area(
            "Describe your vision",
            height=120,
            placeholder="Examples:\n- Create an energetic MrBeast-style video for TikTok\n- Make a professional corporate presentation for YouTube\n- Transform this into an engaging Instagram Reel with vibrant colors",
            help="Be specific about style, mood, and target platform"
        )
    
    with col2:
        st.markdown("### 📱 Target Platforms")
        
        platforms = []
        if st.checkbox("📺 YouTube (16:9)", value=True):
            platforms.append("youtube")
        if st.checkbox("📸 Instagram (9:16)", value=True):
            platforms.append("instagram")
        if st.checkbox("🎵 TikTok (9:16)", value=True):
            platforms.append("tiktok")
        
        st.markdown("### 🎨 Quick Style Presets")
        
        preset = st.selectbox(
            "Choose a preset or use AI auto-detect",
            [
                "🤖 Let AI Decide (Recommended)",
                "⚡ MrBeast Viral Style",
                "🎬 Cinematic & Dramatic",
                "💼 Professional Corporate",
                "📱 Casual Vlog Style",
                "📚 Educational Tutorial"
            ]
        )
        
        if preset != "🤖 Let AI Decide (Recommended)":
            preset_prompts = {
                "⚡ MrBeast Viral Style": " Make it fast-paced and energetic with MrBeast-style yellow subtitles",
                "🎬 Cinematic & Dramatic": " Apply cinematic color grading with dramatic music",
                "💼 Professional Corporate": " Clean, professional style with minimal subtitles",
                "📱 Casual Vlog Style": " Natural vlog feel with balanced pacing",
                "📚 Educational Tutorial": " Clear and focused with standard subtitles"
            }
            if preset in preset_prompts:
                prompt = prompt + preset_prompts[preset]
    
    st.markdown("---")
    
    # Preview AI Plan Button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        if st.button("🧠 Preview AI Analysis", type="secondary", disabled=not uploaded_file or not prompt):
            with st.spinner("AI is analyzing your request..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/analyze/complete",
                        json={"user_prompt": prompt, "platform": "youtube"}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.workflow_plan = data["workflow_plan"]
                        
                        st.markdown("### 🎯 AI Analysis Results")
                        
                        # Key insights
                        insights = data["key_insights"]
                        
                        col_i1, col_i2, col_i3, col_i4 = st.columns(4)
                        
                        with col_i1:
                            st.markdown(f"""
                            <div class="stat-box">
                                <h3>😊</h3>
                                <p><b>Emotion</b></p>
                                <p>{insights['detected_emotion'].title()}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_i2:
                            st.markdown(f"""
                            <div class="stat-box">
                                <h3>🎬</h3>
                                <p><b>Content Type</b></p>
                                <p>{insights['content_type'].title()}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_i3:
                            st.markdown(f"""
                            <div class="stat-box">
                                <h3>✂️</h3>
                                <p><b>Operations</b></p>
                                <p>{insights['total_operations']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_i4:
                            st.markdown(f"""
                            <div class="stat-box">
                                <h3>📊</h3>
                                <p><b>Engagement</b></p>
                                <p>{insights['engagement_score']:.1f}/10</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("### 🎨 AI Creative Decisions")
                        creative = data["workflow_plan"]["creative_decisions"]
                        
                        st.markdown(f"""
                        <div class="feature-box">
                            <p><b>Editing Style:</b> {creative['editing_style']}</p>
                            <p><b>Music Genre:</b> {creative['music_genre']}</p>
                            <p><b>Color Grade:</b> {creative['color_grade']}</p>
                            <p><b>Subtitle Style:</b> {creative['subtitle_style']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"**Estimated Processing Time:** {data['estimated_time']} seconds")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Start Processing Button
    with col_btn2:
        if st.button("🚀 START AI PROCESSING", type="primary", disabled=not uploaded_file or not prompt):
            with st.spinner("Uploading video..."):
                try:
                    # Upload
                    files = {"video": (uploaded_file.name, uploaded_file, "video/mp4")}
                    data = {
                        "prompt": prompt,
                        "platforms": ",".join(platforms)
                    }
                    
                    if music_file:
                        files["music"] = (music_file.name, music_file, "audio/mp3")
                    
                    upload_response = requests.post(
                        f"{API_URL}/api/upload/multiplatform",
                        files=files,
                        data=data
                    )
                    
                    if upload_response.status_code == 200:
                        result = upload_response.json()
                        project_id = result["project_id"]
                        st.session_state.project_id = project_id
                        
                        st.success(f"✅ Video uploaded! Project ID: {project_id}")
                        
                        # Start processing
                        process_response = requests.post(
                            f"{API_URL}/api/process/complete/{project_id}"
                        )
                        
                        if process_response.status_code == 200:
                            st.info("🤖 AI is processing your video through complete workflow...")
                            
                            # Progress tracking
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            phase_text = st.empty()
                            
                            for i in range(100):
                                time.sleep(3)
                                
                                status_response = requests.get(
                                    f"{API_URL}/api/status/{project_id}/detailed"
                                )
                                
                                if status_response.status_code == 200:
                                    status_data = status_response.json()
                                    
                                    progress = status_data.get("progress_percentage", i)
                                    progress_bar.progress(int(progress))
                                    
                                    phase_name = status_data.get("workflow_diagram_phase", "Processing")
                                    phase_text.markdown(f'<div class="phase-indicator">{phase_name}</div>', unsafe_allow_html=True)
                                    status_text.info(status_data.get("status_description", "Processing..."))
                                    
                                    if status_data["status"] == "completed":
                                        progress_bar.progress(100)
                                        
                                        st.markdown("""
                                        <div class="success-box">
                                            <h3>✅ Processing Complete!</h3>
                                            <p>Your video has been optimized for all selected platforms</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Download buttons
                                        st.markdown("### 📥 Download Your Videos")
                                        
                                        dcol1, dcol2, dcol3, dcol4 = st.columns(4)
                                        
                                        with dcol1:
                                            if st.button("📺 YouTube Version"):
                                                video_data = requests.get(
                                                    f"{API_URL}/api/download/{project_id}/youtube"
                                                ).content
                                                st.download_button(
                                                    "⬇️ Download YouTube",
                                                    data=video_data,
                                                    file_name=f"{project_id}_youtube.mp4",
                                                    mime="video/mp4"
                                                )
                                        
                                        with dcol2:
                                            if st.button("📸 Instagram Version"):
                                                video_data = requests.get(
                                                    f"{API_URL}/api/download/{project_id}/instagram"
                                                ).content
                                                st.download_button(
                                                    "⬇️ Download Instagram",
                                                    data=video_data,
                                                    file_name=f"{project_id}_instagram.mp4",
                                                    mime="video/mp4"
                                                )
                                        
                                        with dcol3:
                                            if st.button("🎵 TikTok Version"):
                                                video_data = requests.get(
                                                    f"{API_URL}/api/download/{project_id}/tiktok"
                                                ).content
                                                st.download_button(
                                                    "⬇️ Download TikTok",
                                                    data=video_data,
                                                    file_name=f"{project_id}_tiktok.mp4",
                                                    mime="video/mp4"
                                                )
                                        
                                        with dcol4:
                                            if st.button("🎬 Master Version"):
                                                video_data = requests.get(
                                                    f"{API_URL}/api/download/{project_id}/master"
                                                ).content
                                                st.download_button(
                                                    "⬇️ Download Master",
                                                    data=video_data,
                                                    file_name=f"{project_id}_master.mp4",
                                                    mime="video/mp4"
                                                )
                                        break
                                    
                                    elif status_data["status"] == "failed":
                                        st.error(f"❌ Processing failed: {status_data.get('error', 'Unknown error')}")
                                        break
                
                except Exception as e:
                    st.error(f"Error: {e}")

# ==================== TAB 2: AI ANALYSIS ====================
with tab2:
    st.markdown("## 🧠 AI Brain Analysis")
    
    if st.session_state.workflow_plan:
        plan = st.session_state.workflow_plan
        
        st.markdown("### 📊 Video Analysis")
        analysis = plan["analysis"]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Detected Emotion", analysis["emotion"].title())
        with col2:
            st.metric("Content Type", analysis["content_type"].title())
        with col3:
            st.metric("Quality Score", f"{analysis['quality_score']:.1f}/10")
        
        st.markdown("### 🎨 Creative Decisions")
        creative = plan["creative_decisions"]
        
        st.json(creative)
        
        st.markdown("### ⚙️ Processing Pipeline")
        st.markdown(f"**Total Operations:** {len(plan['operations'])}")
        
        for i, op in enumerate(plan["operations"], 1):
            with st.expander(f"{i}. {op['name'].replace('_', ' ').title()}"):
                st.write(f"**Phase:** {op['phase']}")
                st.write(f"**Priority:** {op['priority']}")
                st.write(f"**Estimated Time:** {op.get('estimated_time', '?')}s")
                if op.get('params'):
                    st.write(f"**Parameters:** {op['params']}")
    else:
        st.info("👈 Upload a video and click 'Preview AI Analysis' to see detailed breakdown")

# ==================== TAB 3: MY PROJECTS ====================
with tab3:
    st.markdown("## 📁 Project History")
    
    if st.button("🔄 Refresh Projects"):
        st.rerun()
    
    try:
        response = requests.get(f"{API_URL}/api/projects")
        if response.status_code == 200:
            projects = response.json()["projects"]
            
            if projects:
                for project in reversed(projects[-10:]):
                    with st.expander(f"🎬 {project['id']} - {project['status'].upper()}"):
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**Created:** {project['created_at']}")
                            st.write(f"**Status:** {project['status']}")
                            st.write(f"**Prompt:** {project['user_prompt']}")
                            
                            if project.get("target_platforms"):
                                platforms_html = "".join([
                                    f'<span class="platform-badge">{p.upper()}</span>'
                                    for p in project["target_platforms"]
                                ])
                                st.markdown(f"**Platforms:** {platforms_html}", unsafe_allow_html=True)
                        
                        with col2:
                            if project["status"] == "completed":
                                st.success("✅ Ready")
                                
                                for platform in project.get("target_platforms", []):
                                    if st.button(f"📥 {platform.upper()}", key=f"{project['id']}_{platform}"):
                                        st.info(f"Download {platform} version")
                            else:
                                st.info(f"Status: {project['status']}")
            else:
                st.info("No projects yet. Create your first video in the 'New Project' tab!")
    except:
        st.error("Cannot connect to backend. Make sure the API is running.")

# ==================== TAB 4: ABOUT ====================
with tab4:
    st.markdown("## About NeuralFlare")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What We Do
        
        NeuralFlare is an AI-powered video editor that understands your content
        and creates platform-optimized videos automatically.
        
        ### ✨ Key Features
        
        - **🧠 Emotion Analysis**: Detects mood and energy in your video
        - **🎨 Creative Decisions**: AI chooses editing style, music, colors
        - **📖 Story Intelligence**: Finds key moments and removes dull parts
        - **📱 Multi-Platform**: One input → Three optimized outputs
        - **⚡ Fast Processing**: Average 2-5 minutes per video
        
        ### 🔄 Workflow
        
        1. Upload raw footage
        2. AI analyzes emotions and content
        3. AI makes creative decisions
        4. Processing pipeline executes
        5. Platform variants generated
        6. Download all versions
        """)
    
    with col2:
        st.markdown("""
        ### 🛠️ Technology Stack
        
        - **AI Brain**: HuggingFace Llama 3
        - **Video Processing**: MoviePy, FFmpeg
        - **Audio Analysis**: Whisper, Librosa
        - **Backend**: FastAPI
        - **Frontend**: Streamlit
        
        ### 📊 Supported Platforms
        
        - YouTube (16:9)
        - Instagram Reels (9:16)
        - TikTok (9:16)
        
        ### 🎵 Music Moods
        
        - Upbeat / Energetic
        - Calm / Relaxing
        - Dramatic / Cinematic
        - Corporate / Professional
        
        ### 🎨 Color Grades
        
        - Warm & Cozy
        - Cool & Professional
        - Vibrant & Saturated
        """)
    
    st.markdown("---")
    st.markdown("### 📈 Stats")
    
    stat1, stat2, stat3, stat4 = st.columns(4)
    
    with stat1:
        st.metric("AI Operations", "15+")
    with stat2:
        st.metric("Platforms", "3")
    with stat3:
        st.metric("Avg Quality", "8.5/10")
    with stat4:
        st.metric("Processing Speed", "2-5 min")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Made with ❤️ for Hackathon | NeuralFlare AI Video Editor v2.0</p>",
    unsafe_allow_html=True
)