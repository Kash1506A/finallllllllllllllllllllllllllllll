import os
import json
import re
import requests
from typing import Dict, List

class AdvancedAIBrain:
    """
    Enhanced AI Brain with:
    - Emotional Intelligence
    - Creative Decision Engine
    - Narrative Restructuring
    - Multi-Platform Optimization
    """
    
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.api_url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        
        self.system_prompt = """You are an advanced AI video editor with emotional intelligence and creative decision-making.

CAPABILITIES:
1. EMOTIONAL INTELLIGENCE: Analyze facial expressions, voice tone, body language
2. CREATIVE DECISIONS: Auto-select styles, music, pacing based on content
3. NARRATIVE RESTRUCTURING: Reorganize footage into story arcs
4. MULTI-PLATFORM: Optimize for YouTube (16:9), Instagram (9:16), TikTok (musical)

AVAILABLE OPERATIONS:
Core Editing:
- remove_fillers: Remove um, uh, ah
- remove_silence: Cut silent parts
- enhance_audio: Noise reduction & normalization
- identify_key_moments: Find crucial scenes (params: emotion_threshold)
- determine_story_message: Understand narrative

Advanced Features:
- analyze_emotions: Detect emotions in video (params: track_faces, analyze_voice)
- add_subtitles: Dynamic subtitles (params: style - "mrbeast"/"standard"/"emotional")
- add_music: Background music (params: mood - "upbeat"/"dramatic"/"calm", volume)
- color_correction: Enhance visual aesthetics (params: mood - "warm"/"cool"/"vibrant")
- rough_cut: Initial edited version
- evaluate_quality: Assess lighting, audio, stability
- platform_optimize: Adapt for platform (params: platform - "youtube"/"instagram"/"tiktok")

Return JSON:
{
    "analysis": {
        "detected_emotion": "energetic/calm/dramatic/educational",
        "content_type": "vlog/tutorial/story/entertainment",
        "key_moments": [{"time": 10.5, "description": "exciting reveal"}],
        "recommended_platform": "youtube/instagram/tiktok"
    },
    "operations": [
        {"name": "analyze_emotions", "priority": 1, "params": {"track_faces": true}},
        {"name": "identify_key_moments", "priority": 2, "params": {"emotion_threshold": 0.7}},
        {"name": "remove_fillers", "priority": 3, "params": {}},
        {"name": "add_music", "priority": 4, "params": {"mood": "upbeat", "volume": 0.2}},
        {"name": "platform_optimize", "priority": 5, "params": {"platform": "youtube"}}
    ],
    "creative_decisions": {
        "editing_style": "fast-paced/slow-burn/dramatic",
        "music_genre": "electronic/acoustic/cinematic",
        "color_grade": "warm/cool/vibrant",
        "subtitle_style": "mrbeast/minimal/elegant"
    },
    "explanation": "Detailed reasoning for choices"
}"""
    
    async def analyze_request(self, user_prompt: str, video_metadata: dict) -> dict:
        """Main analysis with emotion and creative intelligence"""
        try:
            if self.api_key:
                return await self._call_ai_with_intelligence(user_prompt, video_metadata)
            else:
                print("⚠️  No API key, using intelligent fallback")
                return self._intelligent_fallback(user_prompt, video_metadata)
        except Exception as e:
            print(f"⚠️  AI error: {e}, using intelligent fallback")
            return self._intelligent_fallback(user_prompt, video_metadata)
    
    async def _call_ai_with_intelligence(self, prompt: str, metadata: dict) -> dict:
        """Call AI with advanced prompting"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            full_prompt = f"""{self.system_prompt}

VIDEO METADATA:
Duration: {metadata.get('duration', 'unknown')}s
Resolution: {metadata.get('resolution', 'unknown')}
FPS: {metadata.get('fps', 'unknown')}
Has Audio: {metadata.get('has_audio', True)}

USER REQUEST: {prompt}

Analyze the video content, understand the emotion and narrative, then generate a complete JSON editing plan with analysis, operations, and creative decisions."""
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 800,
                    "temperature": 0.75,
                    "top_p": 0.95,
                    "return_full_text": False
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                generated = result[0].get("generated_text", "") if isinstance(result, list) else str(result)
                
                json_match = re.search(r'\{.*\}', generated, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group())
                    
                    # Ensure required structure
                    if "operations" in plan:
                        print(f"✅ AI Brain: {len(plan.get('operations', []))} operations planned")
                        return plan
            
            return self._intelligent_fallback(prompt, metadata)
        
        except Exception as e:
            print(f"⚠️  AI API error: {e}")
            return self._intelligent_fallback(prompt, metadata)
    
    def _intelligent_fallback(self, prompt: str, metadata: dict) -> dict:
        """Rule-based fallback with emotional intelligence"""
        p = prompt.lower()
        duration = metadata.get('duration', 120)
        
        # Detect content type and emotion
        content_analysis = self._analyze_content_intent(p)
        platform = self._detect_target_platform(p)
        
        operations = []
        priority = 1
        
        # Phase 1: Analysis (always first)
        operations.append({
            "name": "analyze_emotions",
            "priority": priority,
            "params": {"track_faces": True, "analyze_voice": True}
        })
        priority += 1
        
        # Phase 2: Identify key moments
        operations.append({
            "name": "identify_key_moments",
            "priority": priority,
            "params": {"emotion_threshold": 0.6}
        })
        priority += 1
        
        # Phase 3: Core editing
        if any(w in p for w in ["filler", "um", "uh", "clean", "professional"]):
            operations.append({
                "name": "remove_fillers",
                "priority": priority,
                "params": {}
            })
            priority += 1
        
        if any(w in p for w in ["silence", "pause", "pace", "fast"]):
            operations.append({
                "name": "remove_silence",
                "priority": priority,
                "params": {}
            })
            priority += 1
        
        if any(w in p for w in ["audio", "sound", "clean", "enhance", "noise"]):
            operations.append({
                "name": "enhance_audio",
                "priority": priority,
                "params": {}
            })
            priority += 1
        
        # Phase 4: Creative enhancements
        if any(w in p for w in ["subtitle", "caption", "text", "word"]):
            style = self._determine_subtitle_style(p, content_analysis)
            operations.append({
                "name": "add_subtitles",
                "priority": priority,
                "params": {"style": style}
            })
            priority += 1
        
        if any(w in p for w in ["music", "background", "sound", "vibe", "mood"]):
            mood = self._determine_music_mood(p, content_analysis)
            operations.append({
                "name": "add_music",
                "priority": priority,
                "params": {"mood": mood, "volume": 0.15}
            })
            priority += 1
        
        if any(w in p for w in ["color", "visual", "aesthetic", "look", "grade"]):
            mood = self._determine_color_mood(p, content_analysis)
            operations.append({
                "name": "color_correction",
                "priority": priority,
                "params": {"mood": mood}
            })
            priority += 1
        
        # Phase 5: Platform optimization
        operations.append({
            "name": "platform_optimize",
            "priority": priority,
            "params": {"platform": platform}
        })
        
        # Build complete response
        return {
            "analysis": {
                "detected_emotion": content_analysis["emotion"],
                "content_type": content_analysis["type"],
                "key_moments": [],
                "recommended_platform": platform
            },
            "operations": operations,
            "creative_decisions": {
                "editing_style": content_analysis["editing_style"],
                "music_genre": self._determine_music_mood(p, content_analysis),
                "color_grade": self._determine_color_mood(p, content_analysis),
                "subtitle_style": self._determine_subtitle_style(p, content_analysis)
            },
            "explanation": f"Intelligent analysis detected {content_analysis['type']} content with {content_analysis['emotion']} emotion. Optimizing for {platform} with {len(operations)} operations."
        }
    
    def _analyze_content_intent(self, prompt: str) -> dict:
        """Analyze what type of content this is"""
        if any(w in prompt for w in ["mrbeast", "viral", "engaging", "exciting", "energy"]):
            return {
                "emotion": "energetic",
                "type": "entertainment",
                "editing_style": "fast-paced"
            }
        elif any(w in prompt for w in ["tutorial", "explain", "teach", "learn", "how to"]):
            return {
                "emotion": "educational",
                "type": "tutorial",
                "editing_style": "clear and focused"
            }
        elif any(w in prompt for w in ["story", "narrative", "journey", "emotional"]):
            return {
                "emotion": "dramatic",
                "type": "story",
                "editing_style": "cinematic"
            }
        elif any(w in prompt for w in ["vlog", "daily", "casual", "personal"]):
            return {
                "emotion": "calm",
                "type": "vlog",
                "editing_style": "natural"
            }
        else:
            return {
                "emotion": "balanced",
                "type": "general",
                "editing_style": "professional"
            }
    
    def _detect_target_platform(self, prompt: str) -> str:
        """Detect which platform to optimize for"""
        if any(w in prompt for w in ["youtube", "long form", "16:9"]):
            return "youtube"
        elif any(w in prompt for w in ["tiktok", "short", "vertical", "music"]):
            return "tiktok"
        elif any(w in prompt for w in ["instagram", "reel", "story", "9:16"]):
            return "instagram"
        else:
            return "youtube"  # Default
    
    def _determine_subtitle_style(self, prompt: str, analysis: dict) -> str:
        """Choose subtitle style based on content"""
        if "mrbeast" in prompt or analysis["emotion"] == "energetic":
            return "mrbeast"
        elif analysis["type"] == "tutorial":
            return "standard"
        elif analysis["emotion"] == "dramatic":
            return "emotional"
        else:
            return "standard"
    
    def _determine_music_mood(self, prompt: str, analysis: dict) -> str:
        """Choose music mood"""
        if any(w in prompt for w in ["upbeat", "energy", "exciting"]):
            return "upbeat"
        elif any(w in prompt for w in ["calm", "relaxing", "peaceful"]):
            return "calm"
        elif any(w in prompt for w in ["dramatic", "intense", "cinematic"]):
            return "dramatic"
        elif analysis["emotion"] == "energetic":
            return "upbeat"
        elif analysis["emotion"] == "dramatic":
            return "dramatic"
        else:
            return "upbeat"
    
    def _determine_color_mood(self, prompt: str, analysis: dict) -> str:
        """Choose color grading mood"""
        if any(w in prompt for w in ["warm", "cozy", "orange"]):
            return "warm"
        elif any(w in prompt for w in ["cool", "blue", "professional"]):
            return "cool"
        elif any(w in prompt for w in ["vibrant", "colorful", "pop"]):
            return "vibrant"
        elif analysis["emotion"] == "energetic":
            return "vibrant"
        elif analysis["type"] == "tutorial":
            return "cool"
        else:
            return "warm"