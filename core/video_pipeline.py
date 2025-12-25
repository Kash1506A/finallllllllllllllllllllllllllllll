# core/video_pipeline.py - UPDATED WITH NEW OPERATIONS

import os
import tempfile
import shutil
from typing import List, Dict
from dataclasses import dataclass, field

# Import all operations
from core.operations.filler_removal import remove_fillers
from core.operations.silence_removal import remove_silence
from core.operations.subtitle_generator import add_subtitles
from core.operations.music_mixer import add_background_music, remove_background_music

# New smart operations
from core.operations.emotion_trimming import trim_by_emotion
from core.operations.emotion_analyzer import analyze_emotions
from core.operations.key_moment_detector import identify_key_moments
from core.operations.color_correction import color_correction
from core.operations.platform_optimizer import platform_optimize
from core.operations.quality_evaluator import evaluate_quality

# Audio operations
from core.operations.audio_enhance import (
    enhance_audio,
    remove_background_noise,
    isolate_voice
)

# Additional operations
from core.operations.additional_operations import (
    stabilization,
    brightness_adjustment,
    add_title,
    face_tracking,
    scene_detection,
    aspect_ratio_convert,
    compression,
    add_filters,
    smart_cut
)

@dataclass
class Operation:
    """Represents a single video editing operation"""
    name: str
    priority: int
    params: Dict = field(default_factory=dict)


class EnhancedVideoPipeline:
    """Complete video processing pipeline"""
    
    def __init__(self):
        self.operations_map = {
            # Core operations
            "remove_fillers": self._op_remove_fillers,
            "remove_silence": self._op_remove_silence,
            "add_subtitles": self._op_add_subtitles,
            "add_music": self._op_add_music,
            
            # Audio operations
            "enhance_audio": self._op_enhance_audio,
            "remove_background_noise": self._op_remove_background_noise,
            "isolate_voice": self._op_isolate_voice,
            
            # NEW: Smart emotion trimming
            "trim_by_emotion": self._op_trim_by_emotion,
            "analyze_emotions": self._op_analyze_emotions,
            "identify_key_moments": self._op_identify_key_moments,
            
            # Visual
            "color_correction": self._op_color_correction,
            "brightness_adjustment": self._op_brightness_adjustment,
            "platform_optimize": self._op_platform_optimize,
            "evaluate_quality": self._op_evaluate_quality,
            
            # Other
            "smart_cut": self._op_smart_cut,
            "stabilization": self._op_stabilization,
            "add_filters": self._op_add_filters,
            "add_title": self._op_add_title,
            "remove_music": self._op_remove_music,
            "face_tracking": self._op_face_tracking,
            "scene_detection": self._op_scene_detection,
            "aspect_ratio": self._op_aspect_ratio,
            "compression": self._op_compression,
        }
        
        self.temp_files = []
        self.metadata = {
            "emotions": [],
            "key_moments": [],
            "quality_metrics": {},
            "scenes": []
        }
    
    def process(
        self,
        input_path: str,
        operations: List[Operation],
        output_path: str = None
    ) -> Dict:
        """Execute video processing pipeline"""
        current_path = input_path
        
        # Sort by priority
        operations = sorted(operations, key=lambda op: op.priority)
        
        print(f"\n🎬 Starting pipeline with {len(operations)} operations")
        print("=" * 60)
        
        for i, operation in enumerate(operations):
            print(f"\n📹 [{i+1}/{len(operations)}] {operation.name.upper()}")
            
            op_func = self.operations_map.get(operation.name)
            if not op_func:
                print(f"    ⚠️ Unknown operation: {operation.name}, skipping")
                continue
            
            temp_output = tempfile.mktemp(suffix=".mp4", dir="data/temp")
            self.temp_files.append(temp_output)
            
            try:
                op_func(current_path, temp_output, **operation.params)
                current_path = temp_output
                print(f"    ✅ Completed successfully")
                
                # Load metadata if generated
                self._load_operation_metadata(temp_output, operation.name)
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                import traceback
                traceback.print_exc()
                print(f"    ⚠️ Continuing with previous output...")
                continue
        
        # Save final output
        if output_path is None:
            output_path = tempfile.mktemp(suffix=".mp4")
        
        shutil.copy2(current_path, output_path)
        self._cleanup()
        
        print("\n" + "=" * 60)
        print("✅ Pipeline completed successfully!")
        print(f"📂 Output: {output_path}")
        print("=" * 60 + "\n")
        
        return {
            "output_path": output_path,
            "metadata": self.metadata
        }
    
    def _load_operation_metadata(self, output_path: str, operation_name: str):
        """Load metadata generated by operations"""
        import json
        
        try:
            if operation_name == "analyze_emotions":
                emotion_file = output_path.replace('.mp4', '_emotions.json')
                if os.path.exists(emotion_file):
                    with open(emotion_file, 'r') as f:
                        self.metadata["emotions"] = json.load(f)
                    os.remove(emotion_file)
            
            elif operation_name == "identify_key_moments":
                moment_file = output_path.replace('.mp4', '_moments.json')
                if os.path.exists(moment_file):
                    with open(moment_file, 'r') as f:
                        self.metadata["key_moments"] = json.load(f)
                    os.remove(moment_file)
            
            elif operation_name == "trim_by_emotion":
                emotion_file = output_path.replace('.mp4', '_emotion_analysis.json')
                if os.path.exists(emotion_file):
                    with open(emotion_file, 'r') as f:
                        self.metadata["emotion_analysis"] = json.load(f)
            
            elif operation_name == "evaluate_quality":
                quality_file = output_path.replace('.mp4', '_quality.json')
                if os.path.exists(quality_file):
                    with open(quality_file, 'r') as f:
                        self.metadata["quality_metrics"] = json.load(f)
                    os.remove(quality_file)
        except:
            pass
    
    # ========== OPERATION WRAPPERS ==========
    
    def _op_remove_fillers(self, input_path: str, output_path: str, **kwargs):
        remove_fillers(input_path, output_path)
    
    def _op_remove_silence(self, input_path: str, output_path: str, **kwargs):
        silence_threshold = kwargs.get("silence_threshold", 0.02)
        min_silence = kwargs.get("min_silence", 0.6)
        remove_silence(input_path, output_path, silence_threshold, min_silence)
    
    def _op_add_subtitles(self, input_path: str, output_path: str, **kwargs):
        style = kwargs.get("style", "standard")
        sync_with_audio = kwargs.get("sync_with_audio", True)
        add_subtitles(input_path, output_path, style, sync_with_audio)
    
    def _op_add_music(self, input_path: str, output_path: str, **kwargs):
        music_path = kwargs.get("music_path")
        volume = kwargs.get("volume", 0.15)
        auto_select = kwargs.get("auto_select", False)
        mood = kwargs.get("mood", "upbeat")
        add_background_music(input_path, output_path, music_path, volume, auto_select, mood)
    
    def _op_enhance_audio(self, input_path: str, output_path: str, **kwargs):
        reduce_noise = kwargs.get("reduce_noise", True)
        normalize = kwargs.get("normalize", True)
        auto_volume = kwargs.get("auto_volume", False)
        enhance_audio(input_path, output_path, reduce_noise, normalize, auto_volume)
    
    def _op_remove_background_noise(self, input_path: str, output_path: str, **kwargs):
        aggressiveness = kwargs.get("aggressiveness", 0.75)
        remove_background_noise(input_path, output_path, aggressiveness)
    
    def _op_isolate_voice(self, input_path: str, output_path: str, **kwargs):
        isolate_voice(input_path, output_path)
    
    def _op_trim_by_emotion(self, input_path: str, output_path: str, **kwargs):
        target_emotion = kwargs.get("target_emotion", None)
        keep_only_engaging = kwargs.get("keep_only_engaging", True)
        trim_by_emotion(input_path, output_path, target_emotion, keep_only_engaging)
    
    def _op_analyze_emotions(self, input_path: str, output_path: str, **kwargs):
        track_faces = kwargs.get("track_faces", True)
        analyze_voice = kwargs.get("analyze_voice", True)
        analyze_emotions(input_path, output_path, track_faces, analyze_voice)
    
    def _op_identify_key_moments(self, input_path: str, output_path: str, **kwargs):
        emotion_threshold = kwargs.get("emotion_threshold", 0.6)
        identify_key_moments(input_path, output_path, emotion_threshold)
    
    def _op_color_correction(self, input_path: str, output_path: str, **kwargs):
        mood = kwargs.get("mood", "warm")
        color_correction(input_path, output_path, mood)
    
    def _op_platform_optimize(self, input_path: str, output_path: str, **kwargs):
        platform = kwargs.get("platform", "youtube")
        platform_optimize(input_path, output_path, platform)
    
    def _op_evaluate_quality(self, input_path: str, output_path: str, **kwargs):
        evaluate_quality(input_path, output_path)
    
    def _op_stabilization(self, input_path: str, output_path: str, **kwargs):
        stabilization(input_path, output_path)
    
    def _op_brightness_adjustment(self, input_path: str, output_path: str, **kwargs):
        brightness_adjustment(input_path, output_path)
    
    def _op_add_title(self, input_path: str, output_path: str, **kwargs):
        title = kwargs.get("title", "Video Title")
        add_title(input_path, output_path, title)
    
    def _op_remove_music(self, input_path: str, output_path: str, **kwargs):
        remove_background_music(input_path, output_path)
    
    def _op_face_tracking(self, input_path: str, output_path: str, **kwargs):
        face_tracking(input_path, output_path)
    
    def _op_scene_detection(self, input_path: str, output_path: str, **kwargs):
        scene_detection(input_path, output_path)
    
    def _op_aspect_ratio(self, input_path: str, output_path: str, **kwargs):
        ratio = kwargs.get("ratio", "16:9")
        aspect_ratio_convert(input_path, output_path, ratio)
    
    def _op_compression(self, input_path: str, output_path: str, **kwargs):
        quality = kwargs.get("quality", "medium")
        compression(input_path, output_path, quality)
    
    def _op_add_filters(self, input_path: str, output_path: str, **kwargs):
        filter_type = kwargs.get("filter", "cinematic")
        add_filters(input_path, output_path, filter_type)
    
    def _op_smart_cut(self, input_path: str, output_path: str, **kwargs):
        smart_cut(input_path, output_path)
    
    def _cleanup(self):
        """Remove temp files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        self.temp_files.clear()


# Backward compatibility
VideoPipeline = EnhancedVideoPipeline