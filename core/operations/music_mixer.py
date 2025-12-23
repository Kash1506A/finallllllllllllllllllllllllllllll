import os
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from moviepy.audio.fx.all import audio_loop

def add_background_music(
    video_path: str,
    output_path: str,
    music_file=None,
    volume: float = 0.15
):
    """Add background music to video"""
    print("    🎵 Adding background music...")
    
    video = VideoFileClip(video_path)
    
    if music_file is None:
        # No music, just copy video
        video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None
        )
        video.close()
        return
    
    # Load music
    if isinstance(music_file, str):
        if not os.path.exists(music_file):
            video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                                verbose=False, logger=None)
            video.close()
            return
        music = AudioFileClip(music_file)
    else:
        # File upload object
        temp = tempfile.mktemp(".mp3")
        with open(temp, "wb") as f:
            f.write(music_file.read())
        music = AudioFileClip(temp)
    
    # Loop music if shorter than video
    if music.duration < video.duration:
        music = audio_loop(music, duration=video.duration)
    else:
        music = music.subclip(0, video.duration)
    
    # Mix audio
    music = music.volumex(volume)
    
    if video.audio:
        final_audio = CompositeAudioClip([video.audio.volumex(1.0), music])
    else:
        final_audio = music
    
    final = video.set_audio(final_audio)
    
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None
    )
    
    video.close()
    final.close()