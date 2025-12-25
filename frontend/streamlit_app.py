# frontend/streamlit_app.py - STUNNING MODERN UI

import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(
    page_title="NeuralFlare AI Video Editor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ULTRA-MODERN CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glass container */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
        padding: 2rem;
        margin: 1rem 0;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Hero header */
    .hero-header {
        text-align: center;
        padding: 3rem 0;
        animation: fadeIn 1s ease-out;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 30px rgba(255, 255, 255, 0.3);
        margin-bottom: 1rem;
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 100px;
        padding: 1.2rem 3rem;
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.2);
        transition: left 0.5s ease;
    }
    
    .stButton>button:hover:before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    /* Upload zone */
    .uploadedFile {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 3px dashed rgba(255, 255, 255, 0.4) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .uploadedFile:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 100%;
        animation: progressShine 2s ease infinite;
    }
    
    @keyframes progressShine {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Status box */
    .status-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        margin: 2rem 0;
        animation: pulse 2s ease infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.85; }
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(17, 153, 142, 0.4);
        animation: successPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes successPop {
        0% {
            opacity: 0;
            transform: scale(0.8);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Download cards */
    .download-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.4s ease;
        border: 2px solid transparent;
        cursor: pointer;
    }
    
    .download-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        border-color: #667eea;
    }
    
    .download-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
    }
    
    /* Platform badges */
    .platform-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 30px;
        margin: 0.3rem;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Spinner */
    .spinner {
        width: 60px;
        height: 60px;
        border: 6px solid rgba(255, 255, 255, 0.2);
        border-top: 6px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        100% { transform: rotate(360deg); }
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 15px;
        color: white;
        font-weight: 600;
        padding: 15px 30px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Text inputs */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Selectbox */
    .stSelectbox {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000"

# Initialize session state
if "project_id" not in st.session_state:
    st.session_state.project_id = None
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False

# HERO SECTION
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🎬 NeuralFlare AI</div>
    <div class="hero-subtitle">Transform Your Videos with Artificial Intelligence</div>
</div>
""", unsafe_allow_html=True)

# FEATURES SHOWCASE
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎨</div>
        <div class="feature-title">AI Enhancement</div>
        <div class="feature-desc">Automatic audio & visual enhancement powered by deep learning</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">😊</div>
        <div class="feature-title">Emotion Detection</div>
        <div class="feature-desc">Keep happy moments, trim boring parts automatically</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Smart Subtitles</div>
        <div class="feature-desc">Auto-generated, perfectly synced captions in multiple styles</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎵</div>
        <div class="feature-title">Music Mixer</div>
        <div class="feature-desc">AI-powered background music with auto-ducking</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# MAIN INTERFACE
tab1, tab2, tab3 = st.tabs(["🚀 Create Video", "📊 My Projects", "💡 Features"])

with tab1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📹 Upload Your Video")
        uploaded_file = st.file_uploader(
            "Drag and drop or click to upload",
            type=["mp4", "mov", "avi", "mkv"],
            help="Max 500MB • MP4, MOV, AVI, MKV"
        )
        
        if uploaded_file:
            file_size = uploaded_file.size / (1024 * 1024)
            st.success(f"✅ {uploaded_file.name} ({file_size:.1f} MB)")
    
    with col2:
        st.markdown("### 🎯 Target Platforms")
        platforms = []
        
        if st.checkbox("📺 YouTube", value=True):
            platforms.append("youtube")
        if st.checkbox("📸 Instagram"):
            platforms.append("instagram")
        if st.checkbox("🎵 TikTok"):
            platforms.append("tiktok")
    
    st.markdown("---")
    
    # PROMPT SECTION
    st.markdown("### 💭 Tell AI What You Want")
    
    example_prompts = [
        "⚡ Leave empty for AUTO mode (AI does everything)",
        "🔊 remove noise and enhance audio",
        "😊 keep happy moments and add music",
        "💬 add subtitles with background music",
        "🎬 make it cinematic with color grading",
        "⚡ remove boring parts, keep exciting content"
    ]
    
    selected_example = st.selectbox(
        "Quick Examples:",
        example_prompts,
        index=0
    )
    
    if selected_example == example_prompts[0]:
        custom_prompt = st.text_area(
            "Your Instructions (or leave empty for AUTO)",
            height=100,
            placeholder="Examples:\n• 'remove noise and enhance audio'\n• 'keep happy moments, add music'\n• 'trim boring parts'\n• Leave empty = AI does EVERYTHING!",
            value=""
        )
    else:
        prompt_value = selected_example.split(" ", 1)[1] if " " in selected_example else selected_example
        custom_prompt = st.text_area(
            "Your Instructions",
            height=100,
            value=prompt_value
        )
    
    # Music upload
    st.markdown("### 🎵 Background Music (Optional)")
    music_file = st.file_uploader(
        "Upload custom music or leave empty for AI selection",
        type=["mp3", "wav", "aac"],
        help="AI will choose appropriate music if left empty"
    )
    
    st.markdown("---")
    
    # PROCESS BUTTON
    can_process = uploaded_file is not None
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(
            "🚀 START AI PROCESSING" if can_process else "⚠️ UPLOAD VIDEO FIRST",
            type="primary",
            disabled=not can_process,
            use_container_width=True
        ):
            with st.spinner("🚀 Uploading and initializing AI..."):
                try:
                    files = {"video": (uploaded_file.name, uploaded_file, "video/mp4")}
                    data = {
                        "prompt": custom_prompt if custom_prompt else "",
                        "platforms": ",".join(platforms) if platforms else "youtube"
                    }
                    
                    if music_file:
                        files["music"] = (music_file.name, music_file, "audio/mp3")
                    
                    # Upload
                    upload_response = requests.post(
                        f"{API_URL}/api/upload/multiplatform",
                        files=files,
                        data=data
                    )
                    
                    if upload_response.status_code == 200:
                        result = upload_response.json()
                        project_id = result["project_id"]
                        st.session_state.project_id = project_id
                        st.session_state.processing_complete = False
                        
                        st.success(f"✅ Project Created: {project_id}")
                        
                        # Start processing
                        process_response = requests.post(
                            f"{API_URL}/api/process/complete/{project_id}"
                        )
                        
                        if process_response.status_code == 200:
                            st.markdown('<div class="status-box">', unsafe_allow_html=True)
                            st.markdown("### 🤖 AI Processing Your Video")
                            st.markdown('<div class="spinner"></div>', unsafe_allow_html=True)
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            max_attempts = 120
                            for i in range(max_attempts):
                                time.sleep(3)
                                
                                status_response = requests.get(
                                    f"{API_URL}/api/status/{project_id}/detailed"
                                )
                                
                                if status_response.status_code == 200:
                                    status_data = status_response.json()
                                    
                                    progress = status_data.get("progress_percentage", 0)
                                    progress_bar.progress(int(progress))
                                    
                                    status_msg = status_data.get("status_description", "Processing...")
                                    status_text.info(f"📊 {status_msg}")
                                    
                                    if status_data["status"] == "completed":
                                        progress_bar.progress(100)
                                        st.session_state.processing_complete = True
                                        st.balloons()
                                        st.success("🎉 PROCESSING COMPLETE!")
                                        time.sleep(2)
                                        st.rerun()
                                        break
                                    
                                    elif status_data["status"] == "failed":
                                        st.error(f"❌ Failed: {status_data.get('error', 'Unknown')}")
                                        break
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Upload failed: {upload_response.text}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # DOWNLOAD SECTION
    if st.session_state.processing_complete and st.session_state.project_id:
        st.markdown("---")
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("## 🎉 Your Video is Ready!")
        st.markdown("### 📥 Download Your Videos")
        
        project_id = st.session_state.project_id
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">📺</div>
                <h3>YouTube</h3>
                <p>16:9 HD Format</p>
            </div>
            """, unsafe_allow_html=True)
            youtube_url = f"{API_URL}/api/download/{project_id}/youtube"
            st.markdown(f"[⬇️ Download]({youtube_url})", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">📸</div>
                <h3>Instagram</h3>
                <p>9:16 Vertical</p>
            </div>
            """, unsafe_allow_html=True)
            instagram_url = f"{API_URL}/api/download/{project_id}/instagram"
            st.markdown(f"[⬇️ Download]({instagram_url})", unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">🎵</div>
                <h3>TikTok</h3>
                <p>9:16 Optimized</p>
            </div>
            """, unsafe_allow_html=True)
            tiktok_url = f"{API_URL}/api/download/{project_id}/tiktok"
            st.markdown(f"[⬇️ Download]({tiktok_url})", unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">🎬</div>
                <h3>Master</h3>
                <p>Full Quality</p>
            </div>
            """, unsafe_allow_html=True)
            master_url = f"{API_URL}/api/download/{project_id}"
            st.markdown(f"[⬇️ Download]({master_url})", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Create New Project", use_container_width=True):
            st.session_state.project_id = None
            st.session_state.processing_complete = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("## 📊 My Projects")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    try:
        response = requests.get(f"{API_URL}/api/projects")
        if response.status_code == 200:
            projects = response.json()["projects"]
            
            if projects:
                for project in reversed(projects[-10:]):
                    status = project['status']
                    
                    status_colors = {
                        'completed': '🟢',
                        'processing': '🟡',
                        'failed': '🔴',
                        'uploaded': '🔵'
                    }
                    
                    status_icon = status_colors.get(status, '⚪')
                    
                    with st.expander(
                        f"{status_icon} {project['id']} - {status.upper()}",
                        expanded=(status == 'completed')
                    ):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Created:** {project.get('created_at', 'N/A')[:19]}")
                            
                            prompt = project.get('user_prompt', '')
                            if prompt:
                                st.markdown(f"**Prompt:** {prompt[:200]}")
                            else:
                                st.info("**Mode:** AUTO (Full AI)")
                            
                            if project.get("platforms"):
                                platforms_html = "".join([
                                    f'<span class="platform-badge">{p.upper()}</span>'
                                    for p in project["platforms"]
                                ])
                                st.markdown(f"**Platforms:** {platforms_html}", unsafe_allow_html=True)
                        
                        with col2:
                            if status == "completed":
                                st.success("✅ READY")
                                pid = project['id']
                                st.markdown(f"[📺 YouTube]({API_URL}/api/download/{pid}/youtube)")
                                st.markdown(f"[📸 Instagram]({API_URL}/api/download/{pid}/instagram)")
                                st.markdown(f"[🎵 TikTok]({API_URL}/api/download/{pid}/tiktok)")
                            elif status == "processing":
                                st.info("⏳ Processing...")
                            elif status == "failed":
                                st.error("❌ Failed")
            else:
                st.info("📁 No projects yet. Create your first video!")
        else:
            st.error("❌ Cannot fetch projects")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("## 💡 Amazing AI Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 😊 Emotion Detection
        - **Auto-detect happy, sad, excited moments**
        - **Filter by emotion:** "keep happy moments"
        - **Remove boring parts automatically**
        - **Smart engagement scoring**
        
        ### 🎵 Smart Music Mixer
        - **Auto-select music by mood**
        - **Volume auto-ducking for voice clarity**
        - **Seamless looping and mixing**
        - **Multiple mood options**
        """)
    
    with col2:
        st.markdown("""
        ### 🎨 AI Enhancement
        - **Noise removal & voice isolation**
        - **Auto color grading**
        - **Brightness & exposure fix**
        - **Platform optimization**
        
        ### 💬 Smart Subtitles
        - **Auto-generated from speech**
        - **Multiple styles (Standard, MrBeast)**
        - **Perfect sync with audio**
        - **Animated text effects**
        """)
    
    st.markdown("---")
    
    st.markdown("### 🚀 How to Use")
    
    st.markdown("""
    **Option 1: AUTO Mode (Recommended)**
    - Leave prompt empty
    - AI applies ALL enhancements automatically
    
    **Option 2: Custom Prompts**
    - "remove noise and enhance audio" → Audio only
    - "keep happy moments" → Emotion filter
    - "add subtitles and music" → Specific features
    
    **Option 3: Emotion-Based**
    - "keep happy moments" → Only happy content
    - "remove boring parts" → Auto-trim dull moments
    - "keep excited moments" → Filter by excitement
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.9);">
    <p style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">✨ NeuralFlare AI Video Editor ✨</p>
    <p style="opacity: 0.8; font-size: 1.1rem;">Powered by Advanced Artificial Intelligence • Made with ❤️</p>
</div>
""", unsafe_allow_html=True)