import streamlit as st
import requests
import time

st.set_page_config(page_title="NeuralFlare AI", layout="wide")

# Backend API URL
API_URL = "http://localhost:8000"

st.title("🎬 NeuralFlare – AI Video Editor")
st.markdown("*Powered by Claude AI Brain*")

# Session state
if "project_id" not in st.session_state:
    st.session_state.project_id = None

# Tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload & Edit", "📊 Projects", "ℹ️ About"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Video")
        uploaded = st.file_uploader("📹 Select video", type=["mp4", "mov", "avi"])
        music = st.file_uploader("🎵 Background Music (optional)", type=["mp3", "wav"])
        
        st.subheader("AI Instructions")
        prompt = st.text_area(
            "Tell AI what to do",
            height=120,
            placeholder="Remove filler words, add MrBeast-style subtitles, clean audio, add background music..."
        )
        
        # Preview AI plan
        if prompt and st.button("🧠 Preview AI Plan"):
            with st.spinner("AI is analyzing..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/analyze",
                        json={
                            "user_prompt": prompt,
                            "platform": "youtube"
                        }
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("AI Plan Generated!")
                        
                        plan = data["plan"]
                        st.write("**Operations:**")
                        for op in plan["operations"]:
                            st.write(f"- {op['name']} (priority: {op['priority']})")
                        
                        st.info(f"**Explanation:** {plan['explanation']}")
                        st.write(f"**Estimated time:** {data['estimated_time']}s")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        st.subheader("Settings")
        platform = st.selectbox(
            "📱 Platform",
            ["YouTube (16:9)", "TikTok/Reels (9:16)", "Instagram (1:1)"]
        )
        
        st.markdown("---")
        st.subheader("Quick Presets")
        if st.button("🎯 MrBeast Style"):
            st.session_state.preset = "Remove filler words, add MrBeast-style yellow subtitles, enhance audio"
        if st.button("🎙️ Podcast Clean"):
            st.session_state.preset = "Remove silence, clean audio, add standard subtitles"
        if st.button("🎬 Cinematic"):
            st.session_state.preset = "Enhance audio, add cinematic music, color grade"
    
    st.markdown("---")
    
    # Process button
    if st.button("🚀 START AI PROCESSING", type="primary", disabled=not uploaded):
        with st.spinner("Uploading video..."):
            try:
                # Upload video
                files = {"video": uploaded.getvalue()}
                data = {"prompt": prompt}
                
                if music:
                    files["music"] = music.getvalue()
                
                response = requests.post(
                    f"{API_URL}/api/upload",
                    files={"video": (uploaded.name, uploaded, "video/mp4")},
                    data={"prompt": prompt}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    project_id = result["project_id"]
                    st.session_state.project_id = project_id
                    
                    st.success(f"✅ Uploaded! Project ID: {project_id}")
                    
                    # Start processing
                    process_response = requests.post(
                        f"{API_URL}/api/process/{project_id}"
                    )
                    
                    if process_response.status_code == 200:
                        st.info("🤖 AI is processing your video...")
                        
                        # Poll status
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i in range(100):
                            time.sleep(2)
                            
                            status_response = requests.get(
                                f"{API_URL}/api/status/{project_id}"
                            )
                            
                            if status_response.status_code == 200:
                                project = status_response.json()
                                
                                if project["status"] == "completed":
                                    progress_bar.progress(100)
                                    st.success("✅ Processing complete!")
                                    
                                    # Download button
                                    st.download_button(
                                        "⬇️ Download Edited Video",
                                        data=requests.get(
                                            f"{API_URL}/api/download/{project_id}"
                                        ).content,
                                        file_name=f"{project_id}_edited.mp4",
                                        mime="video/mp4"
                                    )
                                    break
                                
                                elif project["status"] == "failed":
                                    st.error(f"❌ Processing failed: {project.get('error', 'Unknown error')}")
                                    break
                                
                                else:
                                    progress = min(i + 10, 90)
                                    progress_bar.progress(progress)
                                    status_text.text(f"Status: {project['status']}...")
                
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("Your Projects")
    
    if st.button("🔄 Refresh"):
        st.rerun()
    
    try:
        response = requests.get(f"{API_URL}/api/projects")
        if response.status_code == 200:
            projects = response.json()["projects"]
            
            if projects:
                for project in reversed(projects[-10:]):  # Last 10 projects
                    with st.expander(f"📁 {project['id']} - {project['status']}"):
                        st.write(f"**Created:** {project['created_at']}")
                        st.write(f"**Status:** {project['status']}")
                        st.write(f"**Prompt:** {project['user_prompt']}")
                        
                        if project["status"] == "completed":
                            if st.button(f"⬇️ Download", key=project['id']):
                                video_data = requests.get(
                                    f"{API_URL}/api/download/{project['id']}"
                                ).content
                                st.download_button(
                                    "Save Video",
                                    data=video_data,
                                    file_name=f"{project['id']}_edited.mp4",
                                    mime="video/mp4"
                                )
            else:
                st.info("No projects yet. Upload a video to get started!")
    except:
        st.error("Cannot connect to backend. Make sure the API is running.")

with tab3:
    st.subheader("About NeuralFlare")
    st.markdown("""
    **NeuralFlare** is an AI-powered video editor with a real AI brain that understands your editing intent.
    
    ### Features:
    - 🧠 **AI Brain**: Uses Claude to understand natural language editing requests
    - ✂️ **Smart Editing**: Automatically removes fillers, silence, and enhances audio
    - 💬 **Dynamic Subtitles**: Add MrBeast-style or standard subtitles
    - 🎵 **Music Mixing**: Add and mix background music
    - 📊 **Project Tracking**: Keep history of all your edits
    
    ### Architecture:
    - **Backend**: FastAPI with dynamic video pipeline
    - **AI Brain**: Claude Sonnet 4 for decision making
    - **Database**: JSON-based project tracking
    - **Processing**: MoviePy + Whisper + Librosa
    
    ### How It Works:
    1. You describe what you want in plain English
    2. AI Brain analyzes and plans editing operations
    3. Dynamic pipeline executes operations in optimal order
    4. You get professionally edited video
    
    ---
    Made with ❤️ for hackathon
    """)