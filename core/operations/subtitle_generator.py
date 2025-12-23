import os
import tempfile
import numpy as np
import whisper
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_subtitles(video_path: str, output_path: str, style: str = "standard"):
    """Add animated subtitles to video"""
    print(f"    💬 Adding {style} subtitles...")
    
    model = whisper.load_model("base")
    video = VideoFileClip(video_path)
    
    # Extract audio
    audio_path = tempfile.mktemp(".wav")
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    
    # Transcribe
    result = model.transcribe(audio_path, word_timestamps=True)
    
    subs = []
    
    # Try to load font
    try:
        if style == "mrbeast":
            font = ImageFont.truetype("arialbd.ttf", 52)
        else:
            font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    for seg in result["segments"]:
        words = seg.get("words", [])
        for w in words:
            word = w["word"].strip().upper()
            start = w["start"]
            end = w["end"]
            
            # Detect background brightness
            try:
                frame = video.get_frame(start)
                brightness = np.mean(frame)
            except:
                brightness = 128
            
            # Choose text color
            if style == "mrbeast":
                txt_color = (255, 255, 0, 255)  # Yellow
            else:
                txt_color = (255, 255, 255, 255) if brightness < 120 else (0, 0, 0, 255)
            
            # Create text image
            img = Image.new("RGBA", (video.w, 160), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw text with stroke
            draw.text(
                (video.w // 4, 50),
                word,
                font=font,
                fill=txt_color,
                stroke_width=4,
                stroke_fill=(0, 0, 0, 255)
            )
            
            # Create clip with animation
            clip = ImageClip(np.array(img)).set_start(start).set_duration(end - start)
            
            if style == "mrbeast":
                # Pulse animation
                clip = clip.resize(lambda t: 1 + 0.15 * np.sin(t * 10))
            
            clip = clip.set_position(("center", "bottom"))
            subs.append(clip)
    
    # Composite video with subtitles
    final = CompositeVideoClip([video] + subs)
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None
    )
    
    video.close()
    final.close()
    os.remove(audio_path)