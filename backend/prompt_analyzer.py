# backend/prompt_analyzer.py - INTELLIGENT PROMPT ANALYSIS

import re
from typing import Dict, List, Tuple

class PromptAnalyzer:
    """
    Analyzes user prompts to detect intent and required operations
    """
    
    def __init__(self):
        self.operation_patterns = {
            # Audio operations
            "enhance_audio": [
                r"enhance audio", r"improve audio", r"better audio", 
                r"audio quality", r"clean audio", r"fix audio"
            ],
            "remove_noise": [
                r"remove noise", r"background noise", r"clean noise",
                r"noise reduction", r"denoise"
            ],
            "isolate_voice": [
                r"isolate voice", r"only voice", r"voice only",
                r"extract voice", r"separate voice"
            ],
            "normalize_volume": [
                r"normalize", r"balance volume", r"fix volume",
                r"loud", r"quiet", r"volume balance"
            ],
            
            # Editing operations
            "remove_silence": [
                r"remove silence", r"cut silence", r"trim silence",
                r"skip pauses", r"dead air"
            ],
            "remove_fillers": [
                r"remove filler", r"filler word", r"um uh",
                r"clean speech", r"remove ums"
            ],
            "trim_dull": [
                r"trim dull", r"remove boring", r"keep engaging",
                r"highlight", r"best parts", r"energy"
            ],
            
            # Visual operations
            "color_correction": [
                r"color", r"color grade", r"cinematic",
                r"warm tone", r"cool tone", r"color correction"
            ],
            "brightness": [
                r"brightness", r"exposure", r"lighting",
                r"dark", r"bright", r"fix lighting"
            ],
            "stabilize": [
                r"stabilize", r"shake", r"steady", r"smooth"
            ],
            
            # Subtitles
            "add_subtitles": [
                r"subtitle", r"caption", r"srt", r"text",
                r"subtitles", r"captions"
            ],
            
            # Music
            "add_music": [
                r"add music", r"background music", r"music",
                r"soundtrack", r"bgm"
            ],
            "remove_music": [
                r"remove music", r"no music", r"music off"
            ],
            
            # Platform
            "youtube": [r"youtube", r"yt", r"16:9"],
            "instagram": [r"instagram", r"insta", r"reel", r"ig", r"9:16"],
            "tiktok": [r"tiktok", r"tik tok"],
            
            # Style
            "viral": [r"viral", r"mrbeast", r"fast", r"engaging"],
            "professional": [r"professional", r"polished", r"clean"],
            "cinematic": [r"cinematic", r"movie", r"film"]
        }
        
        self.emotion_keywords = {
            "energetic": ["energetic", "exciting", "viral", "fast", "upbeat"],
            "calm": ["calm", "relaxing", "peaceful", "slow", "soft"],
            "dramatic": ["dramatic", "intense", "emotional", "powerful"],
            "professional": ["professional", "corporate", "business"]
        }
    
    def analyze(self, prompt: str, video_metadata: dict = None) -> Dict:
        """
        Main analysis function
        Returns: detected operations, style, emotion, platform
        """
        prompt_lower = prompt.lower()
        
        # Detect operations
        detected_ops = self._detect_operations(prompt_lower)
        
        # Detect emotion/mood
        emotion = self._detect_emotion(prompt_lower)
        
        # Detect target platform
        platform = self._detect_platform(prompt_lower)
        
        # Detect editing style
        style = self._detect_style(prompt_lower)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(detected_ops, emotion, platform)
        
        return {
            "detected_operations": detected_ops,
            "emotion": emotion,
            "platform": platform,
            "style": style,
            "confidence": confidence,
            "is_auto_mode": len(detected_ops) == 0,
            "prompt_complexity": self._assess_complexity(prompt)
        }
    
    def _detect_operations(self, prompt: str) -> List[str]:
        """Detect which operations user wants"""
        detected = []
        
        for operation, patterns in self.operation_patterns.items():
            if any(re.search(pattern, prompt) for pattern in patterns):
                detected.append(operation)
        
        return detected
    
    def _detect_emotion(self, prompt: str) -> str:
        """Detect emotional tone"""
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in prompt for keyword in keywords):
                return emotion
        return "balanced"
    
    def _detect_platform(self, prompt: str) -> str:
        """Detect target platform"""
        if any(re.search(p, prompt) for p in self.operation_patterns["youtube"]):
            return "youtube"
        elif any(re.search(p, prompt) for p in self.operation_patterns["instagram"]):
            return "instagram"
        elif any(re.search(p, prompt) for p in self.operation_patterns["tiktok"]):
            return "tiktok"
        return "youtube"  # default
    
    def _detect_style(self, prompt: str) -> str:
        """Detect editing style"""
        if "viral" in prompt or "mrbeast" in prompt:
            return "viral"
        elif "cinematic" in prompt or "movie" in prompt:
            return "cinematic"
        elif "professional" in prompt or "corporate" in prompt:
            return "professional"
        return "balanced"
    
    def _calculate_confidence(self, operations: List, emotion: str, platform: str) -> float:
        """Calculate how confident we are about the analysis"""
        score = 0.5  # Base confidence
        
        if len(operations) > 0:
            score += 0.2
        if emotion != "balanced":
            score += 0.15
        if platform != "youtube":  # User specified platform
            score += 0.15
        
        return min(1.0, score)
    
    def _assess_complexity(self, prompt: str) -> str:
        """Assess prompt complexity"""
        word_count = len(prompt.split())
        
        if word_count < 5:
            return "simple"
        elif word_count < 15:
            return "moderate"
        else:
            return "complex"
    
    def generate_summary(self, analysis: Dict) -> str:
        """Generate human-readable summary"""
        if analysis["is_auto_mode"]:
            return "Auto Mode: AI will apply all necessary enhancements"
        
        ops = analysis["detected_operations"]
        emotion = analysis["emotion"]
        platform = analysis["platform"]
        
        summary = f"Detected {len(ops)} operations: {', '.join(ops[:3])}"
        if len(ops) > 3:
            summary += f" + {len(ops) - 3} more"
        
        summary += f" | Mood: {emotion} | Platform: {platform}"
        
        return summary


# Usage example
if __name__ == "__main__":
    analyzer = PromptAnalyzer()
    
    # Test prompts
    test_prompts = [
        "",  # Auto mode
        "remove background noise and add subtitles",
        "make it viral like mrbeast with music",
        "professional corporate video for youtube"
    ]
    
    for prompt in test_prompts:
        print(f"\nPrompt: '{prompt}'")
        analysis = analyzer.analyze(prompt)
        print(f"Analysis: {analyzer.generate_summary(analysis)}")
        print(f"Operations: {analysis['detected_operations']}")