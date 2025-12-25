# core/operations/subtitle_generator.py - COMPLETELY FIXED

import os
import tempfile
import numpy as np
import whisper
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import cv2

def add_subtitles(video_path: str, output_path: str, style: str = "standard", sync_with_audio: bool = True):
    """
    Add animated subtitles - FIXED VERSION
    """
    print(f"    💬 Adding {style} subtitles (synced with audio)...")
    
    video = VideoFileClip(video_path)
    
    if video.audio is None:
        print("    ⚠️  No audio found, cannot generate subtitles")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            verbose=False, logger=None)
        video.close()
        return
    
    try:
        # Extract audio for transcription
        print("       - Extracting audio...")
        audio_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        # Transcribe with word-level timestamps
        print("       - Transcribing audio with Whisper...")
        print("       ⏳ This may take 30-60 seconds...")
        
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, word_timestamps=True, language='en')
        
        total_words = sum(len(seg.get('words', [])) for seg in result['segments'])
        print(f"       ✓ Transcribed {total_words} words in {len(result['segments'])} segments")
        
        # Font settings
        if style == "mrbeast":
            font_size = 80
            text_color = (255, 255, 0, 255)  # Yellow with alpha
            bg_color = (0, 0, 0, 200)  # Black background with transparency
            stroke_width = 5
        else:
            font_size = 65
            text_color = (255, 255, 255, 255)  # White with alpha
            bg_color = (0, 0, 0, 180)  # Black background with transparency
            stroke_width = 4
        
        # Get font
        font = get_font(font_size)
        
        print("       - Creating subtitle clips...")
        
        subtitle_clips = []
        word_count = 0
        errors = 0
        
        for seg_idx, segment in enumerate(result['segments']):
            words = segment.get('words', [])
            
            for word_idx, word_data in enumerate(words):
                try:
                    word = word_data['word'].strip()
                    if not word:
                        continue
                    
                    # Clean word for display
                    word_display = word.upper()
                    
                    start_time = word_data['start']
                    end_time = word_data['end']
                    duration = end_time - start_time
                    
                    if duration < 0.08:  # Skip very short words
                        continue
                    
                    # Create text image
                    img_array = create_subtitle_image(
                        word_display,
                        font,
                        text_color,
                        bg_color,
                        stroke_width,
                        video.w,
                        video.h,
                        style
                    )
                    
                    # Create clip
                    img_clip = ImageClip(img_array).set_duration(duration).set_start(start_time)
                    
                    # Position at bottom center
                    y_pos = int(video.h * 0.80)  # 80% down from top
                    img_clip = img_clip.set_position(('center', y_pos))
                    
                    subtitle_clips.append(img_clip)
                    word_count += 1
                    
                    # Progress indicator
                    if word_count % 20 == 0:
                        print(f"       ... Created {word_count}/{total_words} subtitle clips")
                
                except Exception as e:
                    errors += 1
                    if errors < 5:  # Only show first few errors
                        print(f"       ⚠️  Error with word: {e}")
                    continue
        
        print(f"       ✓ Successfully created {word_count} subtitle clips")
        
        if subtitle_clips:
            # Composite video with subtitles
            print("       - Compositing subtitles with video...")
            final = CompositeVideoClip([video] + subtitle_clips)
            
            # CRITICAL: Preserve audio
            final = final.set_audio(video.audio)
            final = final.set_duration(video.duration)
            
            # Write output
            print("       - Writing output video...")
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
            print(f"       • {word_count} words synchronized")
            print(f"       • Style: {style}")
            print(f"       • Audio preserved: YES")
            
            final.close()
        else:
            print("    ⚠️  No subtitle clips created, preserving original")
            video.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                audio_bitrate="192k",
                verbose=False,
                logger=None
            )
        
        # Cleanup
        video.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)
    
    except Exception as e:
        print(f"    ❌ Subtitle generation error: {e}")
        print(f"    ⚠️  Error details: {type(e).__name__}")
        print("    ↩ Copying original video with audio preserved")
        
        video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            verbose=False,
            logger=None
        )
        video.close()


def get_font(size: int):
    """Get font with fallback options"""
    font_paths = [
        "C:/Windows/Fonts/ariblk.ttf",  # Arial Black - better for subtitles
        "C:/Windows/Fonts/impact.ttf",  # Impact - bold
        "C:/Windows/Fonts/arial.ttf",   # Arial
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
        "/System/Library/Fonts/Helvetica.ttc",  # macOS
    ]
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except:
            continue
    
    print("       ⚠️  Using default font (may not look as good)")
    return ImageFont.load_default()


def create_subtitle_image(text, font, text_color, bg_color, stroke_width, video_w, video_h, style):
    """
    Create subtitle image with text and background
    """
    # Measure text size
    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Get text bounding box
    try:
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0] + stroke_width * 4
        text_height = bbox[3] - bbox[1] + stroke_width * 4
    except:
        # Fallback for older PIL versions
        text_width, text_height = temp_draw.textsize(text, font=font)
        text_width += stroke_width * 4
        text_height += stroke_width * 4
    
    # Add padding
    padding = 20
    img_width = text_width + padding * 2
    img_height = text_height + padding * 2
    
    # Create image
    img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background rectangle (rounded if MrBeast style)
    bg_x1, bg_y1 = padding // 2, padding // 2
    bg_x2, bg_y2 = img_width - padding // 2, img_height - padding // 2
    
    if style == "mrbeast":
        # Rounded rectangle background
        draw.rounded_rectangle(
            [(bg_x1, bg_y1), (bg_x2, bg_y2)],
            radius=15,
            fill=bg_color
        )
    else:
        # Regular rectangle
        draw.rectangle(
            [(bg_x1, bg_y1), (bg_x2, bg_y2)],
            fill=bg_color
        )
    
    # Calculate text position (centered)
    text_x = (img_width - text_width) // 2 + stroke_width * 2
    text_y = (img_height - text_height) // 2 + stroke_width * 2
    
    # Draw text stroke (black outline)
    stroke_color = (0, 0, 0, 255)
    for offset_x in range(-stroke_width, stroke_width + 1):
        for offset_y in range(-stroke_width, stroke_width + 1):
            if offset_x != 0 or offset_y != 0:
                draw.text(
                    (text_x + offset_x, text_y + offset_y),
                    text,
                    font=font,
                    fill=stroke_color
                )
    
    # Draw main text
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    # Convert RGBA to RGB with black background
    background = Image.new('RGB', (video_w, img_height), (0, 0, 0))
    
    # Center the text image
    x_offset = (video_w - img_width) // 2
    
    # Paste with alpha channel
    background.paste(img, (x_offset, 0), img)
    
    return np.array(background)


def add_subtitles_simple(video_path: str, output_path: str):
    """
    Simple subtitle fallback - just preserve video
    """
    print("    💬 Subtitle generation skipped (simple mode)")
    
    video = VideoFileClip(video_path)
    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="192k",
        verbose=False,
        logger=None
    )
    video.close()
    print("    ✅ Video preserved with audio")