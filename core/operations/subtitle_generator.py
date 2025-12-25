# core/operations/subtitle_generator.py - COMPLETELY FIXED (NO CV2 ERRORS)

import os
import tempfile
import numpy as np
import whisper
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_subtitles(video_path: str, output_path: str, style: str = "standard", sync_with_audio: bool = True):
    """
    Add subtitles that SHOW on video - FINAL FIXED VERSION
    """
    print(f"    💬 Adding {style} subtitles...")
    
    video = VideoFileClip(video_path)
    
    if video.audio is None:
        print("    ⚠️  No audio - skipping subtitles")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            verbose=False, logger=None)
        video.close()
        return
    
    try:
        # Extract audio
        print("       - Extracting audio...")
        audio_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        # Transcribe
        print("       - Transcribing with Whisper...")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, word_timestamps=True, language='en')
        
        total_words = sum(len(seg.get('words', [])) for seg in result['segments'])
        print(f"       ✓ Transcribed {total_words} words")
        
        # Settings
        if style == "mrbeast":
            font_size = 70
            color = 'yellow'
            bg_color = 'black'
        else:
            font_size = 60
            color = 'white'
            bg_color = 'black'
        
        print("       - Creating subtitle clips...")
        
        subtitle_clips = []
        word_count = 0
        errors = 0
        
        for segment in result['segments']:
            words = segment.get('words', [])
            
            for word_data in words:
                try:
                    word = word_data['word'].strip()
                    if not word:
                        continue
                    
                    word_display = word.upper() if style == "mrbeast" else word
                    
                    start_time = word_data['start']
                    end_time = word_data['end']
                    duration = end_time - start_time
                    
                    if duration < 0.1:
                        continue
                    
                    # Create subtitle image using PIL only (NO CV2!)
                    img_array = create_subtitle_image_pil(
                        word_display,
                        color,
                        bg_color,
                        video.w,
                        video.h,
                        font_size,
                        style
                    )
                    
                    # Create clip
                    img_clip = ImageClip(img_array).set_duration(duration).set_start(start_time)
                    img_clip = img_clip.set_position(('center', int(video.h * 0.80)))
                    
                    subtitle_clips.append(img_clip)
                    word_count += 1
                    
                    if word_count % 20 == 0:
                        print(f"       ... {word_count}/{total_words} clips created")
                
                except Exception as e:
                    errors += 1
                    if errors <= 3:
                        print(f"       ⚠️  Clip error: {e}")
                    continue
        
        print(f"       ✓ Created {word_count} subtitle clips")
        
        if subtitle_clips:
            # Composite
            print("       - Compositing video with subtitles...")
            final = CompositeVideoClip([video] + subtitle_clips, size=video.size)
            final = final.set_audio(video.audio)
            final = final.set_duration(video.duration)
            
            # Write
            print("       - Rendering final video...")
            final.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=video.fps,
                audio_bitrate="192k",
                preset='medium',
                verbose=False,
                logger=None
            )
            
            print("    ✅ Subtitles added successfully!")
            
            final.close()
            for clip in subtitle_clips:
                clip.close()
        else:
            print("    ⚠️  No clips created - copying original")
            video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                                audio_bitrate="192k", verbose=False, logger=None)
        
        video.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)
    
    except Exception as e:
        print(f"    ❌ Subtitle error: {e}")
        import traceback
        traceback.print_exc()
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()


def create_subtitle_image_pil(text, text_color, bg_color, video_w, video_h, font_size, style):
    """
    Create subtitle image using PIL ONLY (no cv2)
    """
    # Get font
    font = get_font(font_size)
    
    # Create temporary image to measure text
    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Get text size
    try:
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        text_width, text_height = temp_draw.textsize(text, font=font)
    
    # Add padding
    padding = 30
    stroke_width = 4
    
    text_width += stroke_width * 4
    text_height += stroke_width * 4
    
    img_width = min(video_w, text_width + padding * 2)
    img_height = text_height + padding * 2
    
    # Create image with transparent background
    img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background box
    bg_padding = 10
    if style == "mrbeast":
        # Rounded rectangle for MrBeast style
        draw.rounded_rectangle(
            [(bg_padding, bg_padding), (img_width - bg_padding, img_height - bg_padding)],
            radius=15,
            fill=(0, 0, 0, 200)  # Black with transparency
        )
    else:
        # Regular rectangle
        draw.rectangle(
            [(bg_padding, bg_padding), (img_width - bg_padding, img_height - bg_padding)],
            fill=(0, 0, 0, 180)
        )
    
    # Calculate text position (centered)
    text_x = (img_width - text_width) // 2 + stroke_width * 2
    text_y = (img_height - text_height) // 2 + stroke_width * 2
    
    # Convert color names to RGB
    if text_color == 'yellow':
        text_rgb = (255, 255, 0, 255)
    elif text_color == 'white':
        text_rgb = (255, 255, 255, 255)
    else:
        text_rgb = (255, 255, 255, 255)
    
    # Draw black stroke (outline)
    for offset_x in range(-stroke_width, stroke_width + 1):
        for offset_y in range(-stroke_width, stroke_width + 1):
            if offset_x != 0 or offset_y != 0:
                draw.text(
                    (text_x + offset_x, text_y + offset_y),
                    text,
                    font=font,
                    fill=(0, 0, 0, 255)
                )
    
    # Draw main text
    draw.text((text_x, text_y), text, font=font, fill=text_rgb)
    
    # Create final image with black background
    final_img = Image.new('RGB', (video_w, img_height), (0, 0, 0))
    
    # Center the subtitle
    x_offset = (video_w - img_width) // 2
    
    # Paste with alpha
    final_img.paste(img, (x_offset, 0), img)
    
    # Convert to numpy array
    return np.array(final_img)


def get_font(size: int):
    """Get font with multiple fallbacks"""
    font_paths = [
        # Windows
        "C:/Windows/Fonts/ariblk.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arial.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        # Mac
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except Exception as e:
            continue
    
    # Final fallback - use default font
    print("       ℹ️  Using default font")
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()