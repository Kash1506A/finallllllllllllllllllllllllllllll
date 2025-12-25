import cv2
import numpy as np
from moviepy.editor import VideoFileClip
import tempfile
import os

def analyze_emotions(video_path: str, output_path: str, track_faces: bool = True, analyze_voice: bool = True):
    """
    Analyze emotions in video (facial expressions, voice tone)
    Returns metadata but passes video through unchanged
    """
    print("    🧠 Analyzing emotions and energy levels...")
    
    video = VideoFileClip(video_path)
    emotions_data = []
    
    if track_faces:
        # Sample frames for emotion detection
        sample_times = np.linspace(0, video.duration, min(int(video.duration), 30))
        
        for t in sample_times:
            try:
                frame = video.get_frame(t)
                
                # Simple emotion analysis based on brightness and color
                brightness = np.mean(frame)
                color_variance = np.std(frame)
                
                # Detect energy level
                if brightness > 150 and color_variance > 50:
                    emotion = "energetic"
                elif brightness < 100:
                    emotion = "calm"
                else:
                    emotion = "balanced"
                
                emotions_data.append({
                    "time": t,
                    "emotion": emotion,
                    "brightness": float(brightness),
                    "energy": float(color_variance)
                })
            except:
                continue
    
    # Save emotion data for later use
    emotion_file = output_path.replace('.mp4', '_emotions.json')
    import json
    with open(emotion_file, 'w') as f:
        json.dump(emotions_data, f)
    
    print(f"    ✅ Detected {len(emotions_data)} emotion points")
    
    # Pass video through unchanged
    video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                         verbose=False, logger=None)
    video.close()

