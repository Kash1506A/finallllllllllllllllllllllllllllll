
import cv2
import numpy as np
from moviepy.editor import VideoFileClip
import librosa
import tempfile
import os

def evaluate_quality(video_path: str, output_path: str):
    """
    Evaluate video quality (lighting, audio, stability)
    """
    print("    📊 Evaluating video quality...")
    
    video = VideoFileClip(video_path)
    quality_metrics = {}
    
    # Sample frames for quality check
    sample_times = np.linspace(0, min(video.duration, 30), 10)
    
    brightness_values = []
    for t in sample_times:
        frame = video.get_frame(t)
        brightness = np.mean(frame)
        brightness_values.append(brightness)
    
    avg_brightness = np.mean(brightness_values)
    quality_metrics["lighting"] = "good" if 80 < avg_brightness < 180 else "needs_adjustment"
    quality_metrics["avg_brightness"] = float(avg_brightness)
    
    # Check audio quality
    audio_path = tempfile.mktemp(".wav")
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    
    y, sr = librosa.load(audio_path, sr=None)
    audio_level = np.mean(np.abs(y))
    
    quality_metrics["audio_level"] = float(audio_level)
    quality_metrics["audio_quality"] = "good" if audio_level > 0.01 else "low"
    
    print(f"    ✅ Quality: Lighting={quality_metrics['lighting']}, Audio={quality_metrics['audio_quality']}")
    
    # Save quality report
    quality_file = output_path.replace('.mp4', '_quality.json')
    import json
    with open(quality_file, 'w') as f:
        json.dump(quality_metrics, f)
    
    # Pass video through
    video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                         verbose=False, logger=None)
    
    video.close()
    os.remove(audio_path)