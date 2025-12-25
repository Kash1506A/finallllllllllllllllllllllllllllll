# core/operations/emotion_trimming.py - SMART EMOTION TRIMMING

import os
import tempfile
import numpy as np
import librosa
from moviepy.editor import VideoFileClip, concatenate_videoclips
import json
from scipy.ndimage import uniform_filter1d

def trim_by_emotion(video_path: str, output_path: str, target_emotion: str = None, keep_only_engaging: bool = True):
    """
    SMART EMOTION-BASED TRIMMING
    
    If target_emotion specified:
      - Keep only segments matching that emotion
      - Remove all other emotions
    
    If no target_emotion (auto mode):
      - Analyze usefulness
      - Keep engaging/useful parts
      - Remove boring/useless parts
    """
    
    if target_emotion:
        print(f"    💖 EMOTION FILTER: Keeping only '{target_emotion}' moments...")
    else:
        print("    ⚡ SMART TRIMMING: Removing boring parts, keeping engaging content...")
    
    video = VideoFileClip(video_path)
    
    if video.audio is None:
        print("    ⚠️  No audio - keeping full video")
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
        video.close()
        return
    
    try:
        # Extract audio
        print("       - Extracting audio for analysis...")
        audio_path = tempfile.mktemp(".wav", dir="data/temp")
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        
        print("       - Analyzing audio features...")
        
        # AUDIO FEATURE ANALYSIS
        hop_length = sr // 2  # 0.5 second windows
        
        # 1. Energy (RMS)
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        
        # 2. Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
        zcr = librosa.feature.zero_crossing_rate(y=y, hop_length=hop_length)[0]
        
        # 3. Pitch tracking
        try:
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr, hop_length=hop_length)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                pitch_values.append(pitch if pitch > 0 else 0)
            pitch_values = np.array(pitch_values)
        except:
            pitch_values = np.zeros(len(rms))
        
        # 4. MFCCs for emotion detection
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop_length)
        mfcc_mean = np.mean(mfccs, axis=0)
        
        times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=hop_length)
        
        # EMOTION CLASSIFICATION
        emotions = []
        for i in range(len(rms)):
            emotion = classify_emotion(
                rms[i], 
                spectral_centroids[i], 
                zcr[i], 
                pitch_values[i],
                mfcc_mean[i] if i < len(mfcc_mean) else 0
            )
            emotions.append(emotion)
        
        emotions = np.array(emotions)
        
        # Count emotions
        emotion_counts = {}
        for e in emotions:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1
        
        print(f"       - Detected emotions: {emotion_counts}")
        
        # FILTERING LOGIC
        if target_emotion:
            # SPECIFIC EMOTION MODE
            print(f"       - Filtering for '{target_emotion}' moments...")
            
            # Find segments matching target emotion
            target_segments = []
            current_start = None
            
            for i, (t, emotion) in enumerate(zip(times, emotions)):
                if emotion == target_emotion or emotion == "neutral":  # Keep neutral too
                    if current_start is None:
                        current_start = t
                else:
                    if current_start is not None:
                        if t - current_start > 0.5:
                            target_segments.append((current_start, t))
                        current_start = None
            
            if current_start is not None:
                target_segments.append((current_start, video.duration))
            
            segments_to_keep = target_segments
            print(f"       ✓ Found {len(segments_to_keep)} '{target_emotion}' segments")
        
        else:
            # AUTO MODE - Remove boring/useless parts
            print("       - Calculating engagement scores...")
            
            # Normalize features
            def normalize(arr):
                min_val, max_val = np.min(arr), np.max(arr)
                if max_val - min_val == 0:
                    return np.zeros_like(arr)
                return (arr - min_val) / (max_val - min_val)
            
            rms_norm = normalize(rms)
            spec_cent_norm = normalize(spectral_centroids)
            zcr_norm = normalize(zcr)
            pitch_norm = normalize(pitch_values)
            
            # ENGAGEMENT SCORE
            engagement_score = (
                rms_norm * 0.35 +           # Volume importance
                spec_cent_norm * 0.25 +     # Brightness
                zcr_norm * 0.20 +           # Activity
                pitch_norm * 0.20           # Pitch variation
            )
            
            # Smooth
            engagement_score = uniform_filter1d(engagement_score, size=7)
            
            # Penalize "useless" emotions
            for i, emotion in enumerate(emotions):
                if emotion in ["silent", "monotone", "boring"]:
                    engagement_score[i] *= 0.5  # Heavy penalty
            
            # Statistics
            avg_engagement = np.mean(engagement_score)
            std_engagement = np.std(engagement_score)
            
            print(f"       - Average engagement: {avg_engagement:.2f}")
            print(f"       - Variation: {std_engagement:.2f}")
            
            # ADAPTIVE THRESHOLD
            if keep_only_engaging:
                if std_engagement < 0.15:
                    threshold = np.percentile(engagement_score, 25)  # More lenient
                    print("       - Mode: LENIENT (low variation)")
                else:
                    threshold = np.percentile(engagement_score, 40)  # Remove bottom 40%
                    print("       - Mode: AGGRESSIVE (remove boring parts)")
            else:
                threshold = np.percentile(engagement_score, 15)
                print("       - Mode: RELAXED")
            
            print(f"       - Threshold: {threshold:.2f}")
            
            # Find engaging segments
            segments_to_keep = []
            current_start = None
            
            for i, (t, score) in enumerate(zip(times, engagement_score)):
                if score > threshold:
                    if current_start is None:
                        current_start = t
                else:
                    if current_start is not None:
                        if t - current_start > 0.5:
                            segments_to_keep.append((current_start, t))
                        current_start = None
            
            if current_start is not None:
                segments_to_keep.append((current_start, video.duration))
            
            print(f"       ✓ Found {len(segments_to_keep)} engaging segments")
        
        # MERGE CLOSE SEGMENTS
        merged_segments = []
        for start, end in segments_to_keep:
            if merged_segments and start - merged_segments[-1][1] < 1.0:
                merged_segments[-1] = (merged_segments[-1][0], end)
            else:
                merged_segments.append((start, end))
        
        print(f"       ✓ Merged into {len(merged_segments)} final segments")
        
        # Calculate savings
        original_duration = video.duration
        kept_duration = sum([end - start for start, end in merged_segments])
        removed_duration = original_duration - kept_duration
        savings_percent = (removed_duration / original_duration) * 100
        
        print(f"       - Original: {original_duration:.1f}s")
        print(f"       - Kept: {kept_duration:.1f}s ({100-savings_percent:.1f}%)")
        print(f"       - Removed: {removed_duration:.1f}s ({savings_percent:.1f}%)")
        
        # CREATE VIDEO
        if merged_segments and kept_duration > 3.0:
            clips = []
            for i, (start, end) in enumerate(merged_segments):
                if end - start > 0.3:
                    try:
                        clip = video.subclip(start, end)
                        clips.append(clip)
                    except Exception as e:
                        print(f"       ⚠️  Clip error: {e}")
                        continue
            
            if clips:
                print("       - Concatenating segments...")
                final = concatenate_videoclips(clips, method="compose")
                
                final.write_videofile(
                    output_path,
                    codec="libx264",
                    audio_codec="aac",
                    audio_bitrate="192k",
                    preset="medium",
                    verbose=False,
                    logger=None
                )
                
                if target_emotion:
                    print(f"    ✅ EMOTION FILTER COMPLETE - Kept '{target_emotion}' moments")
                else:
                    print(f"    ✅ SMART TRIMMING COMPLETE - Removed {savings_percent:.1f}% boring content")
                
                final.close()
            else:
                print("    ⚠️  No valid clips - keeping original")
                video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                                    audio_bitrate="192k", verbose=False, logger=None)
        else:
            print("    ⚠️  Not enough content - keeping original")
            video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                                audio_bitrate="192k", verbose=False, logger=None)
        
        # Save analysis
        analysis_data = {
            "target_emotion": target_emotion,
            "detected_emotions": emotion_counts,
            "segments": merged_segments,
            "savings_percent": float(savings_percent),
            "timestamps": times.tolist(),
            "emotions_timeline": emotions.tolist()
        }
        
        analysis_file = output_path.replace('.mp4', '_emotion_analysis.json')
        with open(analysis_file, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            audio_bitrate="192k", verbose=False, logger=None)
    
    finally:
        video.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)


def classify_emotion(rms, spectral_centroid, zcr, pitch, mfcc):
    """
    Classify emotion from audio features
    """
    # Silent
    if rms < 0.01:
        return "silent"
    
    # Excited: High energy + high pitch + high brightness
    if rms > 0.15 and spectral_centroid > 2500 and pitch > 200:
        return "excited"
    
    # Happy: Good energy + varied pitch
    if rms > 0.10 and pitch > 150:
        return "happy"
    
    # Sad: Low energy + low pitch
    if rms < 0.08 and pitch < 150:
        return "sad"
    
    # Calm: Medium energy + stable
    if 0.05 < rms < 0.12:
        return "calm"
    
    # Angry: High energy + rough (high ZCR)
    if rms > 0.12 and zcr > 0.1:
        return "angry"
    
    # Boring/monotone: Low variation
    if zcr < 0.05 and pitch < 100:
        return "monotone"
    
    return "neutral"