import os
import tempfile
import librosa
import soundfile as sf
import noisereduce as nr
from moviepy.editor import VideoFileClip, AudioFileClip

def enhance_audio(video_path: str, output_path: str):
    """Enhance audio with noise reduction and normalization"""
    print("    🎧 Enhancing audio quality...")
    
    video = VideoFileClip(video_path)
    
    # Extract audio
    audio_path = tempfile.mktemp(".wav")
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    
    # Load and process
    y, sr = librosa.load(audio_path, sr=None)
    
    # Noise reduction
    y = nr.reduce_noise(y=y, sr=sr)
    
    # Normalize
    y = librosa.util.normalize(y)
    
    # Save cleaned audio
    clean_path = tempfile.mktemp(".wav")
    sf.write(clean_path, y, sr)
    
    # Replace audio in video
    final = video.set_audio(AudioFileClip(clean_path))
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
    os.remove(clean_path)