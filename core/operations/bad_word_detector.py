# core/operations/bad_word_detector.py - BAD WORD DETECTION & MUTING

import os
import tempfile
import whisper
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import numpy as np
import librosa
import soundfile as sf

def detect_bad_words(video_path: str, output_path: str, bad_words: list = None):
    """
    Detect bad words in audio and mute those segments
    """
    print("    🚫 Detecting and muting inappropriate language...")
    
    if bad_words is None:
        bad_words = [
            "fuck", "shit", "damn", "hell", "ass", "bitch",
            "bastard", "crap", "piss", "dick", "cock", "pussy"
        ]
    
    video = VideoFileClip(video_path)
    
    if video.audio is None:
        print("    ⚠️  No audio found")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            verbose=False, logger=None)
        video.close()
        return
    
    try:
        # Extract audio
        audio_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        # Transcribe with word timestamps
        print("       - Transcribing audio to detect bad words...")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, word_timestamps=True)
        
        # Find bad word timestamps
        bad_segments = []
        bad_word_count = 0
        
        for segment in result['segments']:
            for word_data in segment.get('words', []):
                word = word_data['word'].lower().strip()
                
                # Check if word contains bad word
                if any(bad in word for bad in bad_words):
                    start = word_data['start']
                    end = word_data['end']
                    bad_segments.append((start, end))
                    bad_word_count += 1
                    print(f"       🚫 Found inappropriate word at {start:.2f}s - {end:.2f}s")
        
        if bad_word_count == 0:
            print("    ✅ No inappropriate language detected")
            video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                                audio_bitrate="192k", verbose=False, logger=None)
            video.close()
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return
        
        print(f"    ⚠️  Found {bad_word_count} inappropriate words - Muting...")
        
        # Load audio
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        
        # Mute bad segments with smooth fade
        for start, end in bad_segments:
            start_sample = int(start * sr)
            end_sample = int(end * sr)
            
            # Add fade in/out (50ms)
            fade_samples = int(0.05 * sr)
            
            # Fade out
            fade_out_start = max(0, start_sample - fade_samples)
            fade_out_end = start_sample
            if fade_out_end > fade_out_start:
                fade_out = np.linspace(1.0, 0.0, fade_out_end - fade_out_start)
                y[fade_out_start:fade_out_end] *= fade_out
            
            # Mute
            y[start_sample:end_sample] = 0
            
            # Fade in
            fade_in_start = end_sample
            fade_in_end = min(len(y), end_sample + fade_samples)
            if fade_in_end > fade_in_start:
                fade_in = np.linspace(0.0, 1.0, fade_in_end - fade_in_start)
                y[fade_in_start:fade_in_end] *= fade_in
        
        # Save cleaned audio
        clean_audio_path = tempfile.mktemp(suffix=".wav", dir="data/temp")
        sf.write(clean_audio_path, y, sr)
        
        # Replace video audio
        clean_audio = AudioFileClip(clean_audio_path)
        final = video.set_audio(clean_audio)
        
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            verbose=False,
            logger=None
        )
        
        print(f"    ✅ Muted {bad_word_count} inappropriate words successfully")
        
        # Cleanup
        video.close()
        final.close()
        clean_audio.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(clean_audio_path):
            os.remove(clean_audio_path)
    
    except Exception as e:
        print(f"    ❌ Bad word detection error: {e}")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()