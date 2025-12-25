import cv2
import numpy as np
from moviepy.editor import VideoFileClip

def color_correction(video_path: str, output_path: str, mood: str = "warm"):
    """
    Apply color grading based on mood
    """
    print(f"    🎨 Applying {mood} color grading...")
    
    video = VideoFileClip(video_path)
    
    def apply_color_grade(frame):
        """Apply color transformation to frame"""
        frame = frame.astype(np.float32)
        
        if mood == "warm":
            # Increase reds and yellows
            frame[:, :, 0] = np.clip(frame[:, :, 0] * 1.1, 0, 255)  # Red
            frame[:, :, 1] = np.clip(frame[:, :, 1] * 1.05, 0, 255)  # Green
            frame[:, :, 2] = np.clip(frame[:, :, 2] * 0.95, 0, 255)  # Blue
        
        elif mood == "cool":
            # Increase blues
            frame[:, :, 0] = np.clip(frame[:, :, 0] * 0.95, 0, 255)  # Red
            frame[:, :, 1] = np.clip(frame[:, :, 1] * 1.0, 0, 255)   # Green
            frame[:, :, 2] = np.clip(frame[:, :, 2] * 1.1, 0, 255)   # Blue
        
        elif mood == "vibrant":
            # Increase saturation
            frame = np.clip(frame * 1.15, 0, 255)
        
        return frame.astype(np.uint8)
    
    # Apply to all frames
    final = video.fl_image(apply_color_grade)
    final.write_videofile(output_path, codec="libx264", audio_codec="aac",
                         verbose=False, logger=None)
    
    video.close()
    final.close()
