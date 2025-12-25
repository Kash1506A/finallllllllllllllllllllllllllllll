import React, { useState } from 'react';
import axios from 'axios';
import './styles/App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [videoPreview, setVideoPreview] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [projectId, setProjectId] = useState(null);
  const [status, setStatus] = useState('');
  const [progress, setProgress] = useState(0);
  const [aiUnderstanding, setAiUnderstanding] = useState(['Waiting for prompt & video...']);
  const [terminalLogs, setTerminalLogs] = useState(['[AI] System ready.']);
  const [outputs, setOutputs] = useState({
    youtube: null,
    instagram: null,
    tiktok: null,
    master: null
  });
  const [authModal, setAuthModal] = useState(false);
  const [authTab, setAuthTab] = useState('register');

  // Handle video upload
  const handleVideoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setVideoFile(file);
      const url = URL.createObjectURL(file);
      setVideoPreview(url);
      addLog(`Video uploaded: ${file.name}`);
    }
  };

  // Add terminal log
  const addLog = (msg) => {
    setTerminalLogs(prev => [...prev, `[AI] ${msg}`]);
  };

  // Start editing process
  const startEditing = async () => {
    if (!videoFile) {
      alert('Please upload a video first');
      return;
    }

    if (!prompt.trim()) {
      alert('Please enter a prompt describing what you want');
      return;
    }

    try {
      // Update AI Understanding
      setAiUnderstanding([
        '• Analyzing your prompt...',
        '• Detecting required operations',
        '• Planning multi-platform optimization',
        '• YouTube (16:9), Instagram (9:16), TikTok (9:16)',
        '• Preparing emotion analysis',
        '• Setting up audio enhancement'
      ]);

      addLog('Uploading video...');
      
      // Upload video for multi-platform
      const formData = new FormData();
      formData.append('video', videoFile);
      formData.append('prompt', prompt);
      formData.append('platforms', 'youtube,instagram,tiktok');

      const uploadRes = await axios.post(`${API_BASE}/api/upload/multiplatform`, formData);
      const projId = uploadRes.data.project_id;
      setProjectId(projId);
      
      addLog('Video uploaded successfully!');
      addLog('Starting AI analysis...');
      
      // Start processing
      await axios.post(`${API_BASE}/api/process/complete/${projId}`);
      
      setStatus('processing');
      addLog('AI Brain analyzing emotions and planning edits...');
      
      // Poll for status
      pollStatus(projId);
      
    } catch (error) {
      console.error('Error:', error);
      addLog(`Error: ${error.message}`);
      alert('Processing failed. Please try again.');
    }
  };

  // Poll status
  const pollStatus = async (projId) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`${API_BASE}/api/status/${projId}/detailed`);
        const data = res.data;
        
        setStatus(data.status);
        setProgress(data.progress_percentage || 0);
        
        // Update AI Understanding
        if (data.ai_analysis) {
          const analysis = data.ai_analysis;
          setAiUnderstanding([
            `• Mode: ${analysis.mode || 'custom'}`,
            `• Detected emotion: ${analysis.detected_emotion || 'balanced'}`,
            `• Operations: ${analysis.operations_count || 0}`,
            `• Platforms: YouTube, Instagram, TikTok`,
            `• Audio enhancement: Active`,
            `• Subtitle generation: Active`
          ]);
        }
        
        // Add logs based on status
        if (data.status === 'analyzing') {
          addLog('Analyzing emotions and audio features...');
        } else if (data.status === 'processing') {
          addLog('Applying AI-powered edits...');
          addLog('Removing background noise...');
          addLog('Enhancing audio quality...');
          addLog('Analyzing emotions for smart trimming...');
          addLog('Removing boring/dull parts...');
          addLog('Generating synchronized subtitles...');
          addLog('Adding background music...');
          addLog('Optimizing for YouTube (16:9)...');
          addLog('Optimizing for Instagram (9:16)...');
          addLog('Optimizing for TikTok (9:16)...');
        }
        
        if (data.status === 'completed') {
          clearInterval(interval);
          addLog('Processing complete! ✓');
          addLog('All platform versions ready for download');
          
          // Set output paths
          setOutputs({
            youtube: data.output_video,
            instagram: data.output_video,
            tiktok: data.output_video,
            master: data.output_video
          });
        }
        
        if (data.status === 'failed') {
          clearInterval(interval);
          addLog('Processing failed ✗');
          alert('Processing failed. Please try again.');
        }
        
      } catch (error) {
        console.error('Status poll error:', error);
      }
    }, 2000);
  };

  // Download video
  const downloadVideo = (platform) => {
    if (!projectId) return;
    
    const url = `${API_BASE}/api/download/${projectId}/${platform}`;
    window.open(url, '_blank');
    addLog(`Downloading ${platform} version...`);
  };

  return (
    <div className="app">
      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-content">
          <div className="logo">
            VisionCut <span className="logo-ai">AI</span>
          </div>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#how">How it works</a>
            <button onClick={() => setAuthModal(true)} className="btn-link">
              Login
            </button>
            <a href="#studio" className="btn-primary">
              Launch Editor
            </a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>
            Edit Smarter. Create Faster.<br />
            with <span className="highlight">VisionCut AI</span>
          </h1>
          <p>
            Your intelligent video & audio editing assistant.
            Describe what you want — VisionCut AI does the rest.
          </p>
          <a href="#studio" className="btn-hero">
            Start Editing Now
          </a>
        </div>

        {/* Video Grid */}
        <div className="video-grid">
          <div className="video-tile">
            <video autoPlay muted loop playsInline>
              <source src="https://v1.pinimg.com/videos/iht/720p/31/7a/60/317a600b708d9eb97aba1a68749d2545.mp4" type="video/mp4" />
            </video>
            <span className="label">Food</span>
          </div>
          
          <div className="video-tile large">
            <video autoPlay muted loop playsInline>
              <source src="https://filmora.wondershare.com/video/product/res_v-temp5.mp4" type="video/mp4" />
            </video>
            <span className="label">Vloggers</span>
          </div>
          
          <div className="video-tile">
            <video autoPlay muted loop playsInline>
              <source src="https://v1.pinimg.com/videos/iht/720p/9d/be/89/9dbe89ea5b344e4efafed47420c44dcb.mp4" type="video/mp4" />
            </video>
            <span className="label">Gamer</span>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="features">
        <h2>Powerful AI Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>Emotion-Aware Editing</h3>
            <p>Detects tone & energy to keep best moments.</p>
          </div>
          <div className="feature-card">
            <h3>AI Creative Brain</h3>
            <p>Decides pacing & cuts like a director.</p>
          </div>
          <div className="feature-card">
            <h3>Auto Story Structuring</h3>
            <p>Builds engaging narratives automatically.</p>
          </div>
          <div className="feature-card">
            <h3>Multi-Platform Output</h3>
            <p>YouTube, Instagram, TikTok — one click.</p>
          </div>
        </div>
      </section>

      {/* Studio */}
      <section id="studio" className="studio">
        <div className="studio-container">
          <h2>VisionCut AI Studio</h2>

          {/* Upload */}
          <div className="upload-section">
            <h3>Upload Video</h3>
            <label className="upload-label">
              Click to choose a video file
              <input
                type="file"
                accept="video/*"
                onChange={handleVideoUpload}
                hidden
              />
            </label>
            
            {videoPreview && (
              <video
                src={videoPreview}
                controls
                className="video-preview"
              />
            )}
          </div>

          {/* Prompt */}
          <div className="prompt-section">
            <input
              type="text"
              placeholder="Create a fast-paced happy 10s Instagram reel with subtitles and upbeat music..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="prompt-input"
            />
            <button onClick={startEditing} className="btn-start">
              Start Editing
            </button>
          </div>

          {/* AI Understanding */}
          <div className="ai-section">
            <h3>AI Understanding</h3>
            <ul className="ai-list">
              {aiUnderstanding.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>

          {/* Progress */}
          {progress > 0 && (
            <div className="progress-section">
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p>{progress}% Complete - {status}</p>
            </div>
          )}

          {/* Terminal */}
          <div className="terminal">
            {terminalLogs.map((log, i) => (
              <p key={i} dangerouslySetInnerHTML={{ __html: log }} />
            ))}
          </div>

          {/* Output Videos */}
          {status === 'completed' && outputs.master && (
            <div className="output-section">
              <h3>🎉 Your Videos Are Ready!</h3>
              
              <div className="platform-outputs">
                <div className="platform-card">
                  <h4>📺 YouTube (16:9)</h4>
                  <p>Horizontal format for desktop</p>
                  <button
                    onClick={() => downloadVideo('youtube')}
                    className="btn-download"
                  >
                    Download YouTube
                  </button>
                </div>

                <div className="platform-card">
                  <h4>📱 Instagram (9:16)</h4>
                  <p>Vertical reel format</p>
                  <button
                    onClick={() => downloadVideo('instagram')}
                    className="btn-download"
                  >
                    Download Instagram
                  </button>
                </div>

                <div className="platform-card">
                  <h4>🎵 TikTok (9:16)</h4>
                  <p>Vertical short format</p>
                  <button
                    onClick={() => downloadVideo('tiktok')}
                    className="btn-download"
                  >
                    Download TikTok
                  </button>
                </div>

                <div className="platform-card">
                  <h4>🎬 Master Version</h4>
                  <p>Original quality</p>
                  <button
                    onClick={() => downloadVideo('master')}
                    className="btn-download btn-primary"
                  >
                    Download Master
                  </button>
                </div>
              </div>

              {/* Preview */}
              <div className="preview-section">
                <h4>Preview Your Video</h4>
                <video
                  controls
                  className="result-video"
                  src={`${API_BASE}/api/preview/${projectId}`}
                  key={projectId}
                >
                  Your browser doesn't support video playback.
                </video>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Auth Modal */}
      {authModal && (
        <div className="modal-overlay" onClick={() => setAuthModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button
              className="modal-close"
              onClick={() => setAuthModal(false)}
            >
              ×
            </button>

            <div className="modal-tabs">
              <button
                className={authTab === 'register' ? 'active' : ''}
                onClick={() => setAuthTab('register')}
              >
                Register
              </button>
              <button
                className={authTab === 'login' ? 'active' : ''}
                onClick={() => setAuthTab('login')}
              >
                Login
              </button>
            </div>

            {authTab === 'register' ? (
              <div className="auth-form">
                <input type="text" placeholder="Full Name" />
                <input type="email" placeholder="Email" />
                <input type="password" placeholder="Password" />
                <button className="btn-auth">Create Account</button>
                <p className="auth-note">Demo only — stored locally</p>
              </div>
            ) : (
              <div className="auth-form">
                <input type="email" placeholder="Email" />
                <input type="password" placeholder="Password" />
                <button className="btn-auth">Login</button>
                <p className="auth-note">Use the account you registered</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
        © 2025 VisionCut AI. Built for creators.
      </footer>
    </div>
  );
}

export default App;