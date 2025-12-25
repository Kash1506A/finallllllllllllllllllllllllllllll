# backend/ai_brain.py - PROMPT-ONLY MODE (NO AUTO MODE)

import os
import re
from typing import Dict, List

class AdvancedAIBrain:
    """
    AI Brain - ONLY executes operations based on user's prompt
    No automatic operations unless user specifically requests them
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
            "detect_bad_words",
            "adjust_volume",
            "adjust_pitch",
            "brightness_adjustment",
            "color_correction",
            "add_subtitles",
            "add_music",
            "platform_optimize",
            "stabilization",
            "face_tracking",
            "scene_detection",
            "aspect_ratio",
            "compression",
            "add_filters"
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
        
        # Operation detection patterns
        self.operation_patterns = {
            "remove_background_noise": [
                "remove noise", "background noise", "clean noise",
                "noise reduction", "denoise", "remove background"
            ],
            "enhance_audio": [
                "enhance audio", "improve audio", "better audio",
                "audio quality", "clean audio", "fix audio"
            ],
            "isolate_voice": [
                "isolate voice", "only voice", "voice only",
                "extract voice", "separate voice"
            ],
            "remove_silence": [
                "remove silence", "cut silence", "trim silence",
                "skip pauses", "dead air", "silent parts"
            ],
            "remove_fillers": [
                "remove filler", "filler word", "um uh",
                "clean speech", "remove ums", "uh ah"
            ],
            "analyze_emotions": [
                "analyze emotion", "detect emotion", "emotion analysis",
                "facial expression", "mood detection"
            ],
            "trim_by_emotion": [
                "trim boring", "remove boring", "keep engaging",
                "highlight", "best parts", "energy", "keep happy",
                "remove dull", "engaging parts only"
            ],
            "detect_bad_words": [
                "bad word", "profanity", "censor", "mute swear",
                "inappropriate language", "filter language"
            ],
            "brightness_adjustment": [
                "brightness", "exposure", "lighting",
                "dark", "bright", "fix lighting", "adjust brightness"
            ],
            "color_correction": [
                "color", "color grade", "cinematic",
                "warm tone", "cool tone", "color correction"
            ],
            "add_subtitles": [
                "subtitle", "caption", "srt", "text",
                "subtitles", "captions", "add text"
            ],
            "add_music": [
                "add music", "background music", "music",
                "soundtrack", "bgm"
            ],
            "stabilization": [
                "stabilize", "shake", "steady", "smooth"
            ],
            "platform_optimize": [
                "youtube", "instagram", "tiktok", "reel",
                "optimize for", "platform"
            ],
            "aspect_ratio": [
                "aspect ratio", "16:9", "9:16", "1:1",
                "vertical", "horizontal", "square"
            ],
            "add_filters": [
                "filter", "vintage", "cinematic filter",
                "black and white", "bw"
            ]
        }
    
    async def analyze_request(self, user_prompt: str, video_metadata: dict) -> dict:
        """
        PROMPT-ONLY MODE: Only execute what user explicitly asks for
        """
        prompt = (user_prompt or "").strip().lower()
        
        print("\n" + "="*70)
        print("🎯 AI BRAIN - ANALYZING USER REQUEST (PROMPT-ONLY MODE)")
        print("="*70)
        print(f"User Prompt: '{user_prompt}'")
        print(f"Prompt length: {len(prompt)} chars")
        
        # If empty prompt, return error
        if not prompt or len(prompt) < 3:
            print("\n❌ ERROR: Empty prompt! Please specify what you want to do.")
            print("="*70 + "\n")
            return {
                "analysis": {
                    "mode": "error",
                    "error": "Empty prompt - please specify operations"
                },
                "operations": [],
                "creative_decisions": {},
                "explanation": "No operations specified. Please describe what edits you want."
            }
        
        # Detect target emotion (for emotion-based operations)
        target_emotion = self._detect_emotion(prompt)
        
        # Detect platform
        platform = self._detect_platform(prompt)
        
        # Detect which operations user wants
        detected_operations = self._detect_operations_from_prompt(prompt)
        
        # BUILD OPERATION PIPELINE BASED ON USER REQUEST ONLY
        operations = []
        priority = 1
        
        print("\n📋 Building Operation Pipeline from Prompt...")
        print(f"   Mode: PROMPT-ONLY (custom instructions)")
        print(f"   Detected operations: {len(detected_operations)}")
        
        if not detected_operations:
            print("\n⚠️ WARNING: No operations detected in prompt!")
            print("   Please specify what you want to do (e.g., 'remove noise and add subtitles')")
            print("="*70 + "\n")
            return {
                "analysis": {
                    "mode": "error",
                    "error": "No operations detected"
                },
                "operations": [],
                "creative_decisions": {},
                "explanation": "Could not detect any operations from your prompt. Please be more specific."
            }
        
        # Add operations in logical order
        operation_order = [
            "remove_background_noise",
            "enhance_audio",
            "isolate_voice",
            "analyze_emotions",
            "trim_by_emotion",
            "remove_silence",
            "remove_fillers",
            "detect_bad_words",
            "brightness_adjustment",
            "color_correction",
            "stabilization",
            "add_subtitles",
            "add_music",
            "add_filters",
            "aspect_ratio",
            "platform_optimize"
        ]
        
        # Add detected operations in proper order
        for op_name in operation_order:
            if op_name in detected_operations:
                params = self._get_operation_params(op_name, prompt, target_emotion, platform)
                
                operations.append({
                    "name": op_name,
                    "priority": priority,
                    "params": params
                })
                priority += 1
                
                print(f"   ✓ {op_name.replace('_', ' ').title()}")
        
        print(f"\n✅ PIPELINE READY: {len(operations)} operations")
        print("="*70 + "\n")
        
        return {
            "analysis": {
                "mode": "custom",
                "detected_emotion": target_emotion or "none",
                "platform": platform,
                "operations_count": len(operations),
                "user_instructions": True
            },
            "operations": operations,
            "creative_decisions": {
                "target_emotion": target_emotion,
                "platform": platform,
                "operations_requested": [op["name"] for op in operations]
            },
            "explanation": f"Executing {len(operations)} operations based on your request: {', '.join([op['name'].replace('_', ' ') for op in operations])}"
        }
    
    def _detect_operations_from_prompt(self, prompt: str) -> List[str]:
        """Detect which operations user wants from their prompt"""
        detected = []
        
        for operation, patterns in self.operation_patterns.items():
            if any(pattern in prompt for pattern in patterns):
                detected.append(operation)
        
        return detected
    
    def _get_operation_params(self, op_name: str, prompt: str, emotion: str, platform: str) -> dict:
        """Get parameters for operation based on prompt"""
        params = {}
        
        if op_name == "remove_background_noise":
            params = {"aggressiveness": 0.75}
        
        elif op_name == "enhance_audio":
            params = {"reduce_noise": True, "normalize": True, "auto_volume": True}
        
        elif op_name == "remove_silence":
            params = {"silence_threshold": 0.02, "min_silence": 0.5}
        
        elif op_name == "trim_by_emotion":
            params = {
                "target_emotion": emotion,
                "keep_only_engaging": "engaging" in prompt or "boring" in prompt,
                "remove_boring": "boring" in prompt or "dull" in prompt,
                "remove_dull": "dull" in prompt
            }
        
        elif op_name == "analyze_emotions":
            params = {"track_faces": True, "analyze_voice": True}
        
        elif op_name == "brightness_adjustment":
            params = {"auto": True}
        
        elif op_name == "color_correction":
            if "warm" in prompt:
                mood = "warm"
            elif "cool" in prompt:
                mood = "cool"
            elif "vibrant" in prompt:
                mood = "vibrant"
            else:
                mood = self._get_color_mood(emotion)
            params = {"mood": mood}
        
        elif op_name == "add_subtitles":
            style = "mrbeast" if "viral" in prompt or "mrbeast" in prompt else "standard"
            params = {"style": style, "sync_with_audio": True}
        
        elif op_name == "add_music":
            mood = self._get_music_mood(emotion or "upbeat")
            if "upbeat" in prompt:
                mood = "upbeat"
            elif "calm" in prompt:
                mood = "calm"
            elif "dramatic" in prompt:
                mood = "dramatic"
            
            params = {
                "mood": mood,
                "volume": 0.15,
                "auto_select": True,
                "music_path": None
            }
        
        elif op_name == "platform_optimize":
            params = {"platform": platform}
        
        elif op_name == "detect_bad_words":
            params = {"bad_words": self.bad_words}
        
        elif op_name == "aspect_ratio":
            if "9:16" in prompt or "vertical" in prompt:
                ratio = "9:16"
            elif "16:9" in prompt or "horizontal" in prompt:
                ratio = "16:9"
            elif "1:1" in prompt or "square" in prompt:
                ratio = "1:1"
            else:
                ratio = "16:9"
            params = {"ratio": ratio}
        
        elif op_name == "add_filters":
            if "vintage" in prompt:
                filter_type = "vintage"
            elif "bw" in prompt or "black and white" in prompt:
                filter_type = "bw"
            else:
                filter_type = "cinematic"
            params = {"filter": filter_type}
        
        return params
    
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