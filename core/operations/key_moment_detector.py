import librosa
import numpy as np
from moviepy.editor import VideoFileClip
import tempfile
import os

def identify_key_moments(video_path: str, output_path: str, emotion_threshold: float = 0.6):
    """
    Identify key moments in video based on audio energy and visual changes
    """
    print("    ⭐ Identifying key moments and highlights...")
    
    video = VideoFileClip(video_path)
    
    # Extract audio and analyze energy
    audio_path = tempfile.mktemp(".wav")
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    
    y, sr = librosa.load(audio_path, sr=None)
    
    # Calculate audio energy over time
    hop_length = 512
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=hop_length)
    
    # Find peaks (key moments)
    threshold = np.max(rms) * emotion_threshold
    key_moments = []
    
    for i, (t, energy) in enumerate(zip(times, rms)):
        if energy > threshold:
            key_moments.append({
                "time": float(t),
                "energy": float(energy),
                "type": "high_energy"
            })
    
    print(f"    ✅ Found {len(key_moments)} key moments")
    
    # Save key moments
    moment_file = output_path.replace('.mp4', '_moments.json')
    import json
    with open(moment_file, 'w') as f:
        json.dump(key_moments, f)
    
    # Pass video through
    video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                         verbose=False, logger=None)
    video.close()
    os.remove(audio_path)

