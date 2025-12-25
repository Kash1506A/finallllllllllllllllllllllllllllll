# backend/operation_planner.py - INTELLIGENT OPERATION PLANNING

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Operation:
    name: str
    priority: int
    params: Dict
    phase: str
    estimated_time: int

class OperationPlanner:
    """
    Creates optimized operation plans based on detected needs
    """
    
    def __init__(self):
        # Operation phases for proper ordering
        self.phases = {
            "audio_cleanup": 1,
            "audio_enhancement": 2,
            "content_trimming": 3,
            "emotion_analysis": 4,
            "visual_enhancement": 5,
            "text_overlay": 6,
            "music_addition": 7,
            "platform_optimization": 8
        }
        
        # Default operation parameters
        self.default_params = {
            "remove_background_noise": {"aggressiveness": 0.75},
            "isolate_voice": {},
            "enhance_audio": {"reduce_noise": True, "normalize": True, "auto_volume": True},
            "remove_silence": {"silence_threshold": 0.02, "min_silence": 0.5},
            "remove_fillers": {},
            "analyze_emotions": {"track_faces": True, "analyze_voice": True},
            "identify_key_moments": {"emotion_threshold": 0.5},
            "trim_dull_moments": {"keep_only_engaging": True},
            "color_correction": {"mood": "warm"},
            "brightness_adjustment": {"auto": True},
            "add_subtitles": {"style": "standard", "sync_with_audio": True},
            "add_music": {"mood": "upbeat", "volume": 0.15, "auto_select": True},
            "platform_optimize": {"platform": "youtube"}
        }
        
        # Time estimates (seconds)
        self.time_estimates = {
            "remove_background_noise": 30,
            "isolate_voice": 25,
            "enhance_audio": 20,
            "remove_silence": 25,
            "remove_fillers": 35,
            "analyze_emotions": 45,
            "identify_key_moments": 30,
            "trim_dull_moments": 40,
            "color_correction": 30,
            "brightness_adjustment": 15,
            "add_subtitles": 60,
            "add_music": 15,
            "platform_optimize": 20
        }
    
    def create_plan(self, analysis: Dict, user_preferences: Dict = None) -> List[Operation]:
        """
        Create complete operation plan
        """
        if analysis.get("is_auto_mode", False):
            return self._create_auto_plan(analysis)
        else:
            return self._create_custom_plan(analysis, user_preferences)
    
    def _create_auto_plan(self, analysis: Dict) -> List[Operation]:
        """
        Create comprehensive auto plan
        """
        operations = []
        priority = 1
        
        # PHASE 1: Audio Cleanup (CRITICAL)
        operations.append(Operation(
            name="remove_background_noise",
            priority=priority,
            params=self.default_params["remove_background_noise"],
            phase="audio_cleanup",
            estimated_time=self.time_estimates["remove_background_noise"]
        ))
        priority += 1
        
        operations.append(Operation(
            name="isolate_voice",
            priority=priority,
            params=self.default_params["isolate_voice"],
            phase="audio_cleanup",
            estimated_time=self.time_estimates["isolate_voice"]
        ))
        priority += 1
        
        # PHASE 2: Audio Enhancement
        operations.append(Operation(
            name="enhance_audio",
            priority=priority,
            params=self.default_params["enhance_audio"],
            phase="audio_enhancement",
            estimated_time=self.time_estimates["enhance_audio"]
        ))
        priority += 1
        
        # PHASE 3: Content Trimming
        operations.append(Operation(
            name="remove_silence",
            priority=priority,
            params=self.default_params["remove_silence"],
            phase="content_trimming",
            estimated_time=self.time_estimates["remove_silence"]
        ))
        priority += 1
        
        operations.append(Operation(
            name="remove_fillers",
            priority=priority,
            params=self.default_params["remove_fillers"],
            phase="content_trimming",
            estimated_time=self.time_estimates["remove_fillers"]
        ))
        priority += 1
        
        # PHASE 4: Emotion Analysis
        operations.append(Operation(
            name="analyze_emotions",
            priority=priority,
            params=self.default_params["analyze_emotions"],
            phase="emotion_analysis",
            estimated_time=self.time_estimates["analyze_emotions"]
        ))
        priority += 1
        
        operations.append(Operation(
            name="identify_key_moments",
            priority=priority,
            params=self.default_params["identify_key_moments"],
            phase="emotion_analysis",
            estimated_time=self.time_estimates["identify_key_moments"]
        ))
        priority += 1
        
        operations.append(Operation(
            name="trim_dull_moments",
            priority=priority,
            params=self.default_params["trim_dull_moments"],
            phase="emotion_analysis",
            estimated_time=self.time_estimates["trim_dull_moments"]
        ))
        priority += 1
        
        # PHASE 5: Visual Enhancement
        operations.append(Operation(
            name="brightness_adjustment",
            priority=priority,
            params=self.default_params["brightness_adjustment"],
            phase="visual_enhancement",
            estimated_time=self.time_estimates["brightness_adjustment"]
        ))
        priority += 1
        
        operations.append(Operation(
            name="color_correction",
            priority=priority,
            params=self.default_params["color_correction"],
            phase="visual_enhancement",
            estimated_time=self.time_estimates["color_correction"]
        ))
        priority += 1
        
        # PHASE 6: Text Overlay
        operations.append(Operation(
            name="add_subtitles",
            priority=priority,
            params=self.default_params["add_subtitles"],
            phase="text_overlay",
            estimated_time=self.time_estimates["add_subtitles"]
        ))
        priority += 1
        
        # PHASE 7: Music Addition
        operations.append(Operation(
            name="add_music",
            priority=priority,
            params=self.default_params["add_music"],
            phase="music_addition",
            estimated_time=self.time_estimates["add_music"]
        ))
        priority += 1
        
        # PHASE 8: Platform Optimization
        platform = analysis.get("platform", "youtube")
        operations.append(Operation(
            name="platform_optimize",
            priority=priority,
            params={"platform": platform},
            phase="platform_optimization",
            estimated_time=self.time_estimates["platform_optimize"]
        ))
        
        return operations
    
    def _create_custom_plan(self, analysis: Dict, user_preferences: Dict = None) -> List[Operation]:
        """
        Create custom plan based on detected operations
        """
        operations = []
        priority = 1
        
        detected_ops = analysis.get("detected_operations", [])
        emotion = analysis.get("emotion", "balanced")
        platform = analysis.get("platform", "youtube")
        style = analysis.get("style", "balanced")
        
        # Map detected operations to phases
        op_phase_map = {
            "enhance_audio": "audio_enhancement",
            "remove_noise": "audio_cleanup",
            "isolate_voice": "audio_cleanup",
            "normalize_volume": "audio_enhancement",
            "remove_silence": "content_trimming",
            "remove_fillers": "content_trimming",
            "trim_dull": "emotion_analysis",
            "color_correction": "visual_enhancement",
            "brightness": "visual_enhancement",
            "stabilize": "visual_enhancement",
            "add_subtitles": "text_overlay",
            "add_music": "music_addition",
            "remove_music": "music_addition"
        }
        
        # Group operations by phase
        phase_operations = {}
        for op in detected_ops:
            phase = op_phase_map.get(op, "visual_enhancement")
            if phase not in phase_operations:
                phase_operations[phase] = []
            phase_operations[phase].append(op)
        
        # Build operations in phase order
        for phase_name in sorted(self.phases.keys(), key=lambda x: self.phases[x]):
            if phase_name in phase_operations:
                for op_key in phase_operations[phase_name]:
                    # Map detected op to actual operation name
                    op_name = self._map_detected_to_operation(op_key)
                    
                    if op_name:
                        params = self.default_params.get(op_name, {}).copy()
                        
                        # Customize params based on style/emotion
                        params = self._customize_params(op_name, params, emotion, style)
                        
                        operations.append(Operation(
                            name=op_name,
                            priority=priority,
                            params=params,
                            phase=phase_name,
                            estimated_time=self.time_estimates.get(op_name, 30)
                        ))
                        priority += 1
        
        # Always add platform optimization at the end
        operations.append(Operation(
            name="platform_optimize",
            priority=priority,
            params={"platform": platform},
            phase="platform_optimization",
            estimated_time=self.time_estimates["platform_optimize"]
        ))
        
        return operations
    
    def _map_detected_to_operation(self, detected_op: str) -> str:
        """Map detected operation to actual operation name"""
        mapping = {
            "enhance_audio": "enhance_audio",
            "remove_noise": "remove_background_noise",
            "isolate_voice": "isolate_voice",
            "normalize_volume": "enhance_audio",
            "remove_silence": "remove_silence",
            "remove_fillers": "remove_fillers",
            "trim_dull": "trim_dull_moments",
            "color_correction": "color_correction",
            "brightness": "brightness_adjustment",
            "stabilize": "stabilization",
            "add_subtitles": "add_subtitles",
            "add_music": "add_music",
            "remove_music": "remove_music"
        }
        return mapping.get(detected_op)
    
    def _customize_params(self, op_name: str, params: Dict, emotion: str, style: str) -> Dict:
        """Customize operation parameters based on emotion/style"""
        
        if op_name == "add_subtitles":
            if style == "viral":
                params["style"] = "mrbeast"
            else:
                params["style"] = "standard"
        
        elif op_name == "color_correction":
            if emotion == "energetic":
                params["mood"] = "vibrant"
            elif emotion == "calm":
                params["mood"] = "cool"
            elif emotion == "dramatic":
                params["mood"] = "warm"
        
        elif op_name == "add_music":
            if emotion == "energetic":
                params["mood"] = "upbeat"
            elif emotion == "calm":
                params["mood"] = "calm"
            elif emotion == "dramatic":
                params["mood"] = "dramatic"
        
        return params
    
    def calculate_total_time(self, operations: List[Operation]) -> int:
        """Calculate total estimated processing time"""
        return sum(op.estimated_time for op in operations)
    
    def generate_summary(self, operations: List[Operation]) -> str:
        """Generate human-readable summary of the plan"""
        total_time = self.calculate_total_time(operations)
        phases = set(op.phase for op in operations)
        
        summary = f"Plan: {len(operations)} operations across {len(phases)} phases\n"
        summary += f"Estimated time: {total_time // 60}m {total_time % 60}s\n"
        summary += f"Phases: {', '.join(sorted(phases))}"
        
        return summary


# Usage example
if __name__ == "__main__":
    from prompt_analyzer import PromptAnalyzer
    
    analyzer = PromptAnalyzer()
    planner = OperationPlanner()
    
    # Test
    prompt = "remove noise and add subtitles"
    analysis = analyzer.analyze(prompt)
    
    operations = planner.create_plan(analysis)
    
    print(f"Prompt: '{prompt}'")
    print(f"\n{planner.generate_summary(operations)}")
    print("\nOperations:")
    for op in operations:
        print(f"  [{op.priority}] {op.name} ({op.phase}) - {op.estimated_time}s")