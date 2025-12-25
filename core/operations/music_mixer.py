# core/operations/music_mixer.py - FIXED MUSIC SYSTEM

import os
import tempfile
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from moviepy.audio.fx.all import audio_loop
from pydub import AudioSegment
import requests

def add_background_music(
    video_path: str,
    output_path: str,
    music_path=None,
    volume: float = 0.15,
    auto_select: bool = False,
    mood: str = "upbeat"
):
    """
    FIXED: Add background music with proper file handling
    """
    print("    🎵 Adding background music...")
    
    video = VideoFileClip(video_path)
    
    # GET MUSIC FILE
    music_file = None
    
    if music_path and os.path.exists(music_path):
        music_file = music_path
        print(f"       ✓ Using provided music: {os.path.basename(music_path)}")
    
    elif auto_select:
        print(f"       - Auto-selecting {mood} music...")
        music_file = get_music_for_mood(mood)
        
        if not music_file:
            print("       - No local music found, using free music API...")
            music_file = download_free_music(mood)
    
    if not music_file or not os.path.exists(music_file):
        print("    ⚠️  No music available - skipping")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()
        return
    
    try:
        # Load music
        print(f"       - Loading: {os.path.basename(music_file)}")
        music = AudioFileClip(music_file)
        
        # Loop or trim to match video duration
        if music.duration < video.duration:
            print(f"       - Looping music to {video.duration:.1f}s")
            music = audio_loop(music, duration=video.duration)
        else:
            print(f"       - Trimming music to {video.duration:.1f}s")
            music = music.subclip(0, video.duration)
        
        # Set volume
        print(f"       - Setting volume: {volume:.2f}")
        music = music.volumex(volume)
        
        # Mix with video audio
        if video.audio:
            print("       - Mixing with video audio...")
            video_audio = video.audio.volumex(1.0)  # Keep voice at full volume
            final_audio = CompositeAudioClip([video_audio, music])
        else:
            print("       - Using music only (no original audio)")
            final_audio = music
        
        # Set audio
        final = video.set_audio(final_audio)
        
        # Write
        print("       - Rendering final video...")
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            verbose=False,
            logger=None
        )
        
        print("    ✅ Background music added successfully!")
        
        # Cleanup
        video.close()
        final.close()
        music.close()
    
    except Exception as e:
        print(f"    ❌ Music error: {e}")
        import traceback
        traceback.print_exc()
        print("    ↩ Saving without music...")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()


def get_music_for_mood(mood: str) -> str:
    """
    Get local music file for mood
    """
    music_dir = "assets/music"
    os.makedirs(music_dir, exist_ok=True)
    
    # Mood to filename mapping
    mood_files = {
        "upbeat": ["upbeat.mp3", "energetic.mp3", "positive.mp3"],
        "calm": ["calm.mp3", "relaxing.mp3", "peaceful.mp3"],
        "dramatic": ["dramatic.mp3", "intense.mp3", "epic.mp3"],
        "happy": ["happy.mp3", "joyful.mp3", "cheerful.mp3"]
    }
    
    # Check for mood-specific files
    for filename in mood_files.get(mood, ["upbeat.mp3"]):
        filepath = os.path.join(music_dir, filename)
        if os.path.exists(filepath):
            return filepath
    
    # Check for any music file
    for file in os.listdir(music_dir):
        if file.endswith(('.mp3', '.wav', '.aac')):
            return os.path.join(music_dir, file)
    
    return None


def download_free_music(mood: str) -> str:
    """
    Download free background music from free APIs
    
    Using: Free Music Archive or similar free music sources
    """
    try:
        print("       - Attempting to download free music...")
        
        # Create music directory
        music_dir = "assets/music"
        os.makedirs(music_dir, exist_ok=True)
        
        # Free music URLs (royalty-free, Creative Commons)
        # These are placeholder URLs - replace with actual free music sources
        free_music_sources = {
            "upbeat": "https://www.bensound.com/bensound-music/bensound-ukulele.mp3",
            "calm": "https://www.bensound.com/bensound-music/bensound-relaxing.mp3",
            "dramatic": "https://www.bensound.com/bensound-music/bensound-epic.mp3",
            "happy": "https://www.bensound.com/bensound-music/bensound-happy.mp3"
        }
        
        url = free_music_sources.get(mood, free_music_sources["upbeat"])
        output_file = os.path.join(music_dir, f"{mood}_bg.mp3")
        
        # Download
        print(f"       - Downloading from free source...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            print(f"       ✓ Downloaded: {os.path.basename(output_file)}")
            return output_file
        
    except Exception as e:
        print(f"       ⚠️  Download failed: {e}")
    
    return None


def create_default_music_files():
    """
    Helper to create default music files
    
    Instructions for users:
    1. Download royalty-free music from:
       - Bensound.com
       - Free Music Archive
       - YouTube Audio Library
    
    2. Place MP3 files in assets/music/ with these names:
       - upbeat.mp3
       - calm.mp3
       - dramatic.mp3
       - happy.mp3
    """
    music_dir = "assets/music"
    os.makedirs(music_dir, exist_ok=True)
    
    readme = os.path.join(music_dir, "README.txt")
    with open(readme, 'w') as f:
        f.write("""
BACKGROUND MUSIC SETUP
======================

To use background music in NeuralFlare AI:

1. Download royalty-free music from:
   • Bensound.com (free with attribution)
   • Free Music Archive (freemusicarchive.org)
   • YouTube Audio Library
   • Pixabay Music
   • Incompetech.com

2. Place MP3 files in this directory (assets/music/) with these names:
   
   upbeat.mp3      - For energetic/positive videos
   calm.mp3        - For relaxing/peaceful content
   dramatic.mp3    - For intense/epic moments
   happy.mp3       - For joyful content

3. Or just add any MP3 file and the system will use it!

The AI will automatically:
• Loop short music to match video length
• Adjust volume to keep voice clear
• Mix music with video audio

Recommended music length: 2-5 minutes
        """)
    
    print(f"\n💡 Music setup instructions created at: {readme}")
    print("   Please add MP3 files to assets/music/ directory")


def remove_background_music(video_path: str, output_path: str):
    """
    Remove background music (keep voice only)
    """
    print("    🔕 Removing background music...")
    from core.operations.audio_enhance import isolate_voice
    isolate_voice(video_path, output_path)