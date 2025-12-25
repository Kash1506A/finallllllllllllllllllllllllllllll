
from moviepy.editor import VideoFileClip

def platform_optimize(video_path: str, output_path: str, platform: str = "youtube"):
    """
    Optimize video for specific platform (aspect ratio, duration)
    """
    print(f"    📱 Optimizing for {platform}...")
    
    video = VideoFileClip(video_path)
    
    if platform == "youtube":
        # 16:9 format - no change needed usually
        target_aspect = 16/9
        max_duration = None
    
    elif platform == "instagram":
        # 9:16 vertical format
        target_aspect = 9/16
        max_duration = 90  # Instagram reels limit
    
    elif platform == "tiktok":
        # 9:16 vertical format
        target_aspect = 9/16
        max_duration = 60  # TikTok limit
    
    else:
        # Default to YouTube
        target_aspect = 16/9
        max_duration = None
    
    # Crop/resize to target aspect ratio
    current_aspect = video.w / video.h
    
    if abs(current_aspect - target_aspect) > 0.1:
        if target_aspect < current_aspect:
            # Need to crop width
            new_width = int(video.h * target_aspect)
            x_center = video.w // 2
            x1 = x_center - new_width // 2
            x2 = x1 + new_width
            final = video.crop(x1=x1, x2=x2)
        else:
            # Need to crop height
            new_height = int(video.w / target_aspect)
            y_center = video.h // 2
            y1 = y_center - new_height // 2
            y2 = y1 + new_height
            final = video.crop(y1=y1, y2=y2)
    else:
        final = video
    
    # Trim duration if needed
    if max_duration and final.duration > max_duration:
        final = final.subclip(0, max_duration)
        print(f"    ⚠️  Trimmed to {max_duration}s for {platform}")
    
    final.write_videofile(output_path, codec="libx264", audio_codec="aac",
                         verbose=False, logger=None)
    
    video.close()
    if final != video:
        final.close()
