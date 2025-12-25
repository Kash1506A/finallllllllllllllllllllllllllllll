# core/operations/audio_enhance.py - FIXED AUDIO PRESERVATION

import os
import tempfile
import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr
from moviepy.editor import VideoFileClip, AudioFileClip
from scipy import signal
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

def enhance_audio(video_path: str, output_path: str, reduce_noise=True, normalize_audio=True, auto_volume=True):
    """
    FIXED: Enhanced audio with proper preservation
    """
    print("    🎧 Enhancing audio...")
    
    video = VideoFileClip(video_path)
    
    if video.audio is None:
        print("    ⚠️  No audio found")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()
        return
    
    try:
        # Extract audio
        audio_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        # Load
        print("       - Loading audio...")
        audio = AudioSegment.from_wav(audio_path)
        y = np.array(audio.get_array_of_samples()).astype(np.float32)
        sr = audio.frame_rate
        
        # Handle stereo
        if audio.channels == 2:
            y = y.reshape((-1, 2))
            y = np.mean(y, axis=1)
        
        y = y / (2**15)  # Normalize to -1 to 1
        
        # Noise reduction
        if reduce_noise:
            print("       - Removing noise...")
            try:
                noise_sample = y[:int(0.5 * sr)]
                y = nr.reduce_noise(
                    y=y,
                    sr=sr,
                    y_noise=noise_sample,
                    stationary=False,
                    prop_decrease=0.7
                )
            except Exception as e:
                print(f"       ⚠️  Noise reduction error: {e}")
        
        # Auto volume balance
        if auto_volume:
            print("       - Balancing volume...")
            rms = np.sqrt(np.mean(y**2))
            if rms > 0:
                target_rms = 0.15
                factor = np.clip(target_rms / rms, 0.5, 3.0)
                y = y * factor
                print(f"       ✓ Volume adjusted by {factor:.2f}x")
        
        # Dynamic range compression
        print("       - Compressing dynamics...")
        y_int = (y * 32767).astype(np.int16)
        audio_compressed = AudioSegment(
            y_int.tobytes(),
            frame_rate=sr,
            sample_width=2,
            channels=1
        )
        audio_compressed = compress_dynamic_range(audio_compressed, threshold=-20.0, ratio=4.0)
        
        # Normalize
        if normalize_audio:
            print("       - Normalizing...")
            audio_compressed = normalize(audio_compressed, headroom=3.0)
        
        # High-pass filter
        print("       - Removing low rumble...")
        y_final = np.array(audio_compressed.get_array_of_samples()).astype(np.float32) / 32767.0
        sos = signal.butter(4, 80, 'hp', fs=sr, output='sos')
        y_final = signal.sosfilt(sos, y_final)
        
        # Save
        clean_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        sf.write(clean_path, y_final, sr)
        
        # Merge
        print("       - Merging with video...")
        clean_audio = AudioFileClip(clean_path)
        final = video.set_audio(clean_audio)
        
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            verbose=False,
            logger=None
        )
        
        print("    ✅ Audio enhanced!")
        
        # Cleanup
        video.close()
        final.close()
        clean_audio.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(clean_path):
            os.remove(clean_path)
    
    except Exception as e:
        print(f"    ❌ Audio enhance error: {e}")
        print("    ⏩ Copying original...")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()


def remove_background_noise(video_path: str, output_path: str, aggressiveness=0.75):
    """FIXED: Remove noise while preserving audio"""
    print(f"    🔇 Removing background noise...")
    
    video = VideoFileClip(video_path)
    
    if video.audio is None:
        print("    ⚠️  No audio")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()
        return
    
    try:
        audio_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        
        noise_sample = y[:int(0.5 * sr)]
        y_clean = nr.reduce_noise(
            y=y,
            sr=sr,
            y_noise=noise_sample,
            prop_decrease=aggressiveness
        )
        
        # Normalize
        peak = np.abs(y_clean).max()
        if peak > 0:
            y_clean = y_clean * (0.7 / peak)
        
        clean_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        sf.write(clean_path, y_clean, sr)
        
        clean_audio = AudioFileClip(clean_path)
        final = video.set_audio(clean_audio)
        
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            verbose=False,
            logger=None
        )
        
        print("    ✅ Noise removed!")
        
        video.close()
        final.close()
        clean_audio.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(clean_path):
            os.remove(clean_path)
    
    except Exception as e:
        print(f"    ❌ Error: {e}")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()


def isolate_voice(video_path: str, output_path: str):
    """FIXED: Isolate voice while preserving audio quality"""
    print("    🎙️ Isolating voice...")
    
    video = VideoFileClip(video_path)
    
    if video.audio is None:
        print("    ⚠️  No audio")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()
        return
    
    try:
        audio_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        
        # Aggressive noise reduction
        y = nr.reduce_noise(y=y, sr=sr, prop_decrease=0.85)
        
        # Voice frequency band-pass (100Hz - 4000Hz)
        sos_low = signal.butter(6, 100, 'hp', fs=sr, output='sos')
        sos_high = signal.butter(6, 4000, 'lp', fs=sr, output='sos')
        y = signal.sosfilt(sos_low, y)
        y = signal.sosfilt(sos_high, y)
        
        # Gate quiet parts
        rms = librosa.feature.rms(y=y, hop_length=512)[0]
        threshold = np.median(rms) * 0.3
        hop_length = 512
        mask = rms > threshold
        mask = np.repeat(mask, hop_length)[:len(y)]
        y = y * mask
        
        # Normalize
        peak = np.abs(y).max()
        if peak > 0:
            y = y * (0.75 / peak)
        
        clean_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        sf.write(clean_path, y, sr)
        
        clean_audio = AudioFileClip(clean_path)
        final = video.set_audio(clean_audio)
        
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            verbose=False,
            logger=None
        )
        
        print("    ✅ Voice isolated!")
        
        video.close()
        final.close()
        clean_audio.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(clean_path):
            os.remove(clean_path)
    
    except Exception as e:
        print(f"    ❌ Error: {e}")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()