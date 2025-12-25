# backend/ai_brain.py - COMPLETELY FIXED VERSION

import os
import re
from typing import Dict, List

class AdvancedAIBrain:
    """Fixed AI Brain - Respects prompts correctly"""
    
    def __init__(self):
        # Emotion keywords for filtering
        self.emotion_keywords = {
            "happy": ["happy", "joy", "joyful", "cheerful", "positive", "smile", "laugh"],
            "sad": ["sad", "sadness", "depressing", "melancholic", "crying"],
            "excited": ["excited", "exciting", "energetic", "thrilling", "enthusiastic"],
            "calm": ["calm", "peaceful", "relaxing", "serene", "tranquil"],
            "angry": ["angry", "anger", "furious", "rage", "mad"],
        }
        
        # Operation detection patterns
        self.patterns = {
            # Audio operations
            "remove_noise": ["noise", "background noise", "clean audio", "denoise"],
            "enhance_audio": ["enhance audio", "improve audio", "better sound", "audio quality"],
            "isolate_voice": ["voice only", "isolate voice", "extract voice"],
            
            # Emotion operations
            "emotion_filter": ["keep happy", "keep sad", "keep excited", "keep calm", "keep angry", 
                              "only happy", "only sad", "happy moments", "excited parts"],
            "trim_boring": ["remove boring", "trim boring", "cut boring", "keep engaging", "remove dull"],
            
            # Content operations
            "remove_silence": ["silence", "remove silence", "cut silence", "skip pauses"],
            "remove_fillers": ["filler", "um", "uh", "remove filler"],
            
            # Visual operations
            "add_subtitles": ["subtitle", "caption", "add text", "srt"],
            "add_music": ["music", "background music", "add music", "soundtrack"],
            "color_correction": ["color", "color grade", "cinematic"],
        }
    
    async def analyze_request(self, user_prompt: str, video_metadata: dict) -> dict:
        """Main analysis - FIXED to respect user prompts"""
        prompt = (user_prompt or "").strip().lower()
        
        print("\n" + "="*70)
        print("🎯 AI BRAIN ANALYSIS")
        print("="*70)
        print(f"User Prompt: '{user_prompt}'")
        print(f"Prompt Length: {len(prompt)}")
        
        # CHECK: Empty prompt = AUTO MODE
        if len(prompt) < 3:
            print("🤖 MODE: FULL AUTO (Empty prompt)")
            return self._full_auto_mode()
        
        # USER GAVE PROMPT - Analyze it
        print("🎯 MODE: CUSTOM (User gave instructions)")
        return self._analyze_custom_prompt(prompt)
    
    def _analyze_custom_prompt(self, prompt: str) -> dict:
        """Analyze custom prompt and create operations"""
        operations = []
        priority = 1
        detected = set()
        
        print("\n🔍 Analyzing prompt for operations...")
        
        # STEP 1: Detect target emotion (if any)
        target_emotion = None
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    target_emotion = emotion
                    print(f"✅ Target Emotion: {emotion}")
                    detected.add("emotion_filter")
                    break
            if target_emotion:
                break
        
        # STEP 2: Detect all requested operations
        for op_name, keywords in self.patterns.items():
            for keyword in keywords:
                if keyword in prompt:
                    detected.add(op_name)
                    print(f"✅ Detected: {op_name} ('{keyword}')")
                    break
        
        print(f"\n📋 Total operations detected: {len(detected)}")
        
        # BUILD OPERATION LIST IN CORRECT ORDER
        
        # PHASE 1: AUDIO OPERATIONS (if requested)
        if "remove_noise" in detected:
            operations.append({
                "name": "remove_background_noise",
                "priority": priority,
                "params": {"aggressiveness": 0.75}
            })
            priority += 1
            print("   → Will remove background noise")
        
        if "isolate_voice" in detected:
            operations.append({
                "name": "isolate_voice",
                "priority": priority,
                "params": {}
            })
            priority += 1
            print("   → Will isolate voice")
        
        if "enhance_audio" in detected:
            operations.append({
                "name": "enhance_audio",
                "priority": priority,
                "params": {"reduce_noise": True, "normalize": True, "auto_volume": True}
            })
            priority += 1
            print("   → Will enhance audio")
        
        # PHASE 2: EMOTION-BASED TRIMMING
        if target_emotion or "emotion_filter" in detected or "trim_boring" in detected:
            # Always analyze emotions first
            operations.append({
                "name": "analyze_emotions",
                "priority": priority,
                "params": {"track_faces": True, "analyze_voice": True}
            })
            priority += 1
            print("   → Will analyze emotions")
            
            # Then trim based on emotion
            operations.append({
                "name": "trim_by_emotion",
                "priority": priority,
                "params": {
                    "target_emotion": target_emotion,
                    "keep_only_engaging": target_emotion is None
                }
            })
            priority += 1
            if target_emotion:
                print(f"   → Will keep only '{target_emotion}' moments")
            else:
                print("   → Will remove boring parts automatically")
        
        # PHASE 3: CONTENT TRIMMING
        if "remove_silence" in detected:
            operations.append({
                "name": "remove_silence",
                "priority": priority,
                "params": {"silence_threshold": 0.02, "min_silence": 0.5}
            })
            priority += 1
            print("   → Will remove silence")
        
        if "remove_fillers" in detected:
            operations.append({
                "name": "remove_fillers",
                "priority": priority,
                "params": {}
            })
            priority += 1
            print("   → Will remove filler words")
        
        # PHASE 4: VISUAL ENHANCEMENTS
        if "color_correction" in detected:
            operations.append({
                "name": "color_correction",
                "priority": priority,
                "params": {"mood": "warm"}
            })
            priority += 1
            print("   → Will apply color correction")
        
        # PHASE 5: SUBTITLES (Always add if requested)
        if "add_subtitles" in detected:
            style = "mrbeast" if "viral" in prompt or "mrbeast" in prompt else "standard"
            operations.append({
                "name": "add_subtitles",
                "priority": priority,
                "params": {"style": style, "sync_with_audio": True}
            })
            priority += 1
            print(f"   → Will add subtitles (style: {style})")
        
        # PHASE 6: BACKGROUND MUSIC (Critical fix)
        if "add_music" in detected:
            mood = self._detect_music_mood(prompt)
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
            print(f"   → Will add background music ({mood} mood)")
        
        # PHASE 7: PLATFORM OPTIMIZATION (always at end)
        platform = self._detect_platform(prompt)
        operations.append({
            "name": "platform_optimize",
            "priority": priority,
            "params": {"platform": platform}
        })
        print(f"   → Platform: {platform}")
        
        print(f"\n✅ Final plan: {len(operations)} operations")
        print("="*70 + "\n")
        
        return {
            "analysis": {
                "mode": "custom",
                "detected_emotion": target_emotion or "any",
                "operations_count": len(operations)
            },
            "operations": operations,
            "creative_decisions": {
                "target_emotion": target_emotion,
                "trim_boring": "trim_boring" in detected or target_emotion is not None
            },
            "explanation": f"Applying {len(operations)} operations as requested"
        }
    
    def _full_auto_mode(self) -> dict:
        """Full AUTO mode - Apply ALL enhancements"""
        print("\n🤖 FULL AUTO MODE - Applying all AI enhancements")
        
        operations = []
        priority = 1
        
        # Audio cleanup
        operations.append({"name": "remove_background_noise", "priority": priority, 
                          "params": {"aggressiveness": 0.75}})
        priority += 1
        
        operations.append({"name": "enhance_audio", "priority": priority,
                          "params": {"reduce_noise": True, "normalize": True, "auto_volume": True}})
        priority += 1
        
        # Emotion analysis + smart trimming
        operations.append({"name": "analyze_emotions", "priority": priority,
                          "params": {"track_faces": True, "analyze_voice": True}})
        priority += 1
        
        operations.append({"name": "trim_by_emotion", "priority": priority,
                          "params": {"target_emotion": None, "keep_only_engaging": True}})
        priority += 1
        
        # Remove silence
        operations.append({"name": "remove_silence", "priority": priority,
                          "params": {"silence_threshold": 0.02, "min_silence": 0.5}})
        priority += 1
        
        # Visual
        operations.append({"name": "color_correction", "priority": priority,
                          "params": {"mood": "warm"}})
        priority += 1
        
        # Subtitles
        operations.append({"name": "add_subtitles", "priority": priority,
                          "params": {"style": "standard", "sync_with_audio": True}})
        priority += 1
        
        # Music
        operations.append({"name": "add_music", "priority": priority,
                          "params": {"mood": "upbeat", "volume": 0.15, "auto_select": True}})
        priority += 1
        
        # Platform
        operations.append({"name": "platform_optimize", "priority": priority,
                          "params": {"platform": "youtube"}})
        
        print(f"✅ AUTO MODE: {len(operations)} operations planned")
        print("="*70 + "\n")
        
        return {
            "analysis": {"mode": "auto", "operations_count": len(operations)},
            "operations": operations,
            "creative_decisions": {"auto_mode": True},
            "explanation": f"AUTO MODE: Applying {len(operations)} AI operations"
        }
    
    def _detect_music_mood(self, prompt: str) -> str:
        """Detect music mood from prompt"""
        if any(w in prompt for w in ["upbeat", "energetic", "exciting", "happy"]):
            return "upbeat"
        elif any(w in prompt for w in ["calm", "relaxing", "peaceful"]):
            return "calm"
        elif any(w in prompt for w in ["dramatic", "intense", "epic"]):
            return "dramatic"
        return "upbeat"
    
    def _detect_platform(self, prompt: str) -> str:
        """Detect target platform"""
        if "youtube" in prompt or "yt" in prompt:
            return "youtube"
        elif "instagram" in prompt or "insta" in prompt or "reel" in prompt:
            return "instagram"
        elif "tiktok" in prompt:
            return "tiktok"
        return "youtube"