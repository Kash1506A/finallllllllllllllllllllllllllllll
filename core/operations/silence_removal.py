import os
import tempfile
import librosa
from moviepy.editor import VideoFileClip, concatenate_videoclips

def remove_silence(
    video_path: str,
    output_path: str,
    silence_threshold: float = 0.02,
    min_silence: float = 0.6
):
    """Remove silent parts from video"""
    print("    🔇 Detecting and removing silence...")
    
    video = VideoFileClip(video_path)
    
    # Extract audio
    audio_path = tempfile.mktemp(".wav")
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    
    # Analyze audio
    y, sr = librosa.load(audio_path, sr=None)
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.frames_to_time(range(len(rms)), sr=sr)
    
    # Find non-silent segments
    keep = []
    start = 0.0
    silent_start = None
    
    for i, energy in enumerate(rms):
        t = times[i]
        if energy < silence_threshold:
            if silent_start is None:
                silent_start = t
        else:
            if silent_start is not None:
                if (t - silent_start) >= min_silence:
                    keep.append((start, silent_start))
                    start = t
                silent_start = None
    
    if start < video.duration:
        keep.append((start, video.duration))
    
    # Create clips
    clips = [video.subclip(s, e) for s, e in keep if e - s > 0.2]
    
    if clips:
        final = concatenate_videoclips(clips)
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None
        )
        final.close()
    else:
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            verbose=False, logger=None)
    
    video.close()
    os.remove(audio_path)