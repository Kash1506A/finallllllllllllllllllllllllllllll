# backend/ai_brain.py - COMPLETE AI BRAIN WITH ALL OPERATIONS

import os
import re
from typing import Dict, List

class AdvancedAIBrain:
    """
    Complete AI Brain - Handles ALL operations automatically
    """
    
    def __init__(self):
        # ALL supported operations
        self.all_operations = [
            "remove_background_noise",
            "enhance_audio",
            "isolate_voice",
            "analyze_emotions",
            "trim_by_emotion",
            "remove_silence",
            "remove_fillers",
            "detect_bad_words",  # NEW
            "adjust_volume",  # NEW
            "adjust_pitch",  # NEW
            "brightness_adjustment",
            "color_correction",
            "add_subtitles",
            "add_music",
            "platform_optimize"
        ]
        
        # Emotion keywords
        self.emotion_keywords = {
            "happy": ["happy", "joy", "joyful", "cheerful", "positive"],
            "excited": ["excited", "energetic", "viral", "fast"],
            "calm": ["calm", "peaceful", "relaxing", "slow"],
            "sad": ["sad", "emotional", "touching"],
            "dramatic": ["dramatic", "intense", "epic"]
        }
        
        # Bad words list (profanity filter)
        self.bad_words = [
            "fuck", "shit", "damn", "hell", "ass", "bitch",
            "bastard", "crap", "piss", "dick", "cock"
        ]
    
    async def analyze_request(self, user_prompt: str, video_metadata: dict) -> dict:
        """
        Main AI Brain - Analyzes and creates operation plan based on prompt
        """
        prompt = (user_prompt or "").strip().lower()
        
        print("\n" + "="*70)
        print("🎯 AI BRAIN - ANALYZING USER REQUEST")
        print("="*70)
        print(f"User Prompt: '{user_prompt}'")
        print(f"Prompt length: {len(prompt)} chars")
        
        # Check if user gave specific instructions
        has_instructions = self._has_specific_instructions(prompt)
        
        # Detect target emotion
        target_emotion = self._detect_emotion(prompt)
        
        # Detect platform
        platform = self._detect_platform(prompt)
        
        # Check what user wants
        user_wants = self._analyze_user_wants(prompt)
        
        # BUILD OPERATION PIPELINE BASED ON USER REQUEST
        operations = []
        priority = 1
        
        print("\n📋 Building Operation Pipeline...")
        print(f"   Mode: {'CUSTOM (user instructions)' if has_instructions else 'AUTO (full AI)'}")
        
        # ===== ALWAYS: Audio Enhancement =====
        print("\n🎧 AUDIO PROCESSING:")
        
        if user_wants.get('remove_noise') or not has_instructions:
            operations.append({
                "name": "remove_background_noise",
                "priority": priority,
                "params": {"aggressiveness": 0.75}
            })
            priority += 1
            print("   ✓ Remove background noise")
        
        if user_wants.get('enhance_audio') or not has_instructions:
            operations.append({
                "name": "enhance_audio",
                "priority": priority,
                "params": {"reduce_noise": True, "normalize": True, "auto_volume": True}
            })
            priority += 1
            print("   ✓ Enhance audio quality")
        
        # Bad word detection (always on)
        operations.append({
            "name": "detect_bad_words",
            "priority": priority,
            "params": {"bad_words": self.bad_words}
        })
        priority += 1
        print("   ✓ Bad word detection")
        
        # ===== EMOTION ANALYSIS (if requested OR auto mode) =====
        if target_emotion or user_wants.get('emotion_based') or not has_instructions:
            print("\n💖 EMOTION ANALYSIS:")
            
            operations.append({
                "name": "analyze_emotions",
                "priority": priority,
                "params": {"track_faces": True, "analyze_voice": True}
            })
            priority += 1
            print("   ✓ Analyze emotions")
            
            operations.append({
                "name": "trim_by_emotion",
                "priority": priority,
                "params": {
                    "target_emotion": target_emotion,
                    "keep_only_engaging": True,
                    "remove_boring": user_wants.get('remove_boring', not has_instructions),
                    "remove_dull": user_wants.get('remove_dull', not has_instructions)
                }
            })
            priority += 1
            if target_emotion:
                print(f"   ✓ Keep '{target_emotion}' moments only")
            else:
                print("   ✓ Remove boring/dull parts")
        
        # ===== CONTENT TRIMMING =====
        if user_wants.get('remove_silence') or not has_instructions:
            print("\n✂️ CONTENT TRIMMING:")
            
            operations.append({
                "name": "remove_silence",
                "priority": priority,
                "params": {"silence_threshold": 0.02, "min_silence": 0.5}
            })
            priority += 1
            print("   ✓ Remove silence")
        
        if user_wants.get('remove_fillers') or not has_instructions:
            operations.append({
                "name": "remove_fillers",
                "priority": priority,
                "params": {}
            })
            priority += 1
            print("   ✓ Remove filler words")
        
        # ===== VISUAL ENHANCEMENTS =====
        if user_wants.get('adjust_brightness') or not has_instructions:
            print("\n🎨 VISUAL ENHANCEMENT:")
            
            operations.append({
                "name": "brightness_adjustment",
                "priority": priority,
                "params": {"auto": True}
            })
            priority += 1
            print("   ✓ Adjust brightness")
        
        if user_wants.get('color_correction') or not has_instructions:
            operations.append({
                "name": "color_correction",
                "priority": priority,
                "params": {"mood": self._get_color_mood(target_emotion)}
            })
            priority += 1
            print("   ✓ Color correction")
        
        # ===== SUBTITLES (if requested) =====
        if user_wants.get('add_subtitles'):
            print("\n💬 SUBTITLES:")
            
            style = "mrbeast" if "viral" in prompt or "mrbeast" in prompt else "standard"
            operations.append({
                "name": "add_subtitles",
                "priority": priority,
                "params": {"style": style, "sync_with_audio": True}
            })
            priority += 1
            print(f"   ✓ Add subtitles ({style})")
        
        # ===== MUSIC (if requested) =====
        if user_wants.get('add_music'):
            print("\n🎵 BACKGROUND MUSIC:")
            
            mood = self._get_music_mood(target_emotion or "upbeat")
            operations.append({
                "name": "add_music",
                "priority": priority,
                "params": {
                    "mood": mood,
                    "volume": 0.15,
                    "auto_select": True,
                    "music_path": None
                }
            })
            priority += 1
            print(f"   ✓ Add music ({mood})")
        
        # ===== PLATFORM OPTIMIZATION (always) =====
        print("\n📱 PLATFORM OPTIMIZATION:")
        operations.append({
            "name": "platform_optimize",
            "priority": priority,
            "params": {"platform": platform}
        })
        priority += 1
        print(f"   ✓ Optimize for {platform}")
        
        print(f"\n✅ PIPELINE READY: {len(operations)} operations")
        print("="*70 + "\n")
        
        return {
            "analysis": {
                "mode": "custom" if has_instructions else "auto",
                "detected_emotion": target_emotion or "balanced",
                "platform": platform,
                "operations_count": len(operations),
                "user_instructions": has_instructions
            },
            "operations": operations,
            "creative_decisions": {
                "target_emotion": target_emotion,
                "trim_boring": user_wants.get('remove_boring', not has_instructions),
                "remove_dull": user_wants.get('remove_dull', not has_instructions),
                "bad_word_filter": True,
                "audio_enhancement": True,
                "visual_enhancement": user_wants.get('adjust_brightness', not has_instructions)
            },
            "explanation": f"Pipeline with {len(operations)} operations based on your request"
        }
    
    def _has_specific_instructions(self, prompt: str) -> bool:
        """Check if user gave specific instructions"""
        keywords = [
            'add', 'remove', 'subtitle', 'music', 'trim', 'cut',
            'enhance', 'adjust', 'brightness', 'color', 'filter',
            'silence', 'filler', 'noise', 'emotion', 'happy', 'sad'
        ]
        return any(keyword in prompt for keyword in keywords)
    
    def _analyze_user_wants(self, prompt: str) -> dict:
        """Analyze what user specifically wants"""
        wants = {
            'remove_noise': any(w in prompt for w in ['noise', 'clean audio', 'remove background']),
            'enhance_audio': any(w in prompt for w in ['enhance audio', 'better audio', 'improve audio']),
            'remove_silence': any(w in prompt for w in ['silence', 'remove silence', 'cut silence']),
            'remove_fillers': any(w in prompt for w in ['filler', 'um', 'uh', 'remove filler']),
            'remove_boring': any(w in prompt for w in ['boring', 'dull', 'trim boring', 'engaging']),
            'remove_dull': any(w in prompt for w in ['dull', 'useless', 'trim dull']),
            'add_subtitles': any(w in prompt for w in ['subtitle', 'caption', 'text', 'srt']),
            'add_music': any(w in prompt for w in ['music', 'background music', 'soundtrack']),
            'adjust_brightness': any(w in prompt for w in ['brightness', 'lighting', 'exposure']),
            'color_correction': any(w in prompt for w in ['color', 'grade', 'cinematic']),
            'emotion_based': any(w in prompt for w in ['happy', 'sad', 'excited', 'calm', 'emotion', 'reel'])
        }
        return wants
    
    def _detect_emotion(self, prompt: str) -> str:
        """Detect target emotion from prompt"""
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in prompt for keyword in keywords):
                return emotion
        return None
    
    def _detect_platform(self, prompt: str) -> str:
        """Detect target platform"""
        if "youtube" in prompt or "yt" in prompt:
            return "youtube"
        elif "instagram" in prompt or "insta" in prompt or "reel" in prompt:
            return "instagram"
        elif "tiktok" in prompt:
            return "tiktok"
        return "youtube"  # Default
    
    def _get_music_mood(self, emotion: str) -> str:
        """Get music mood based on emotion"""
        mood_map = {
            "happy": "upbeat",
            "excited": "upbeat",
            "calm": "calm",
            "sad": "emotional",
            "dramatic": "dramatic"
        }
        return mood_map.get(emotion, "upbeat")
    
    def _get_color_mood(self, emotion: str) -> str:
        """Get color grading mood"""
        color_map = {
            "happy": "warm",
            "excited": "vibrant",
            "calm": "cool",
            "sad": "cool",
            "dramatic": "warm"
        }
        return color_map.get(emotion, "warm")