import os
import tempfile
import shutil
from typing import List, Dict
from dataclasses import dataclass, field

from core.operations.filler_removal import remove_fillers
from core.operations.silence_removal import remove_silence
from core.operations.audio_enhance import enhance_audio
from core.operations.subtitle_generator import add_subtitles
from core.operations.music_mixer import add_background_music

@dataclass
class Operation:
    """Represents a single video editing operation"""
    name: str
    priority: int
    params: Dict = field(default_factory=dict)

class VideoPipeline:
    """Dynamic video processing pipeline"""
    
    def __init__(self):
        self.operations_map = {
            "remove_fillers": self._op_remove_fillers,
            "remove_silence": self._op_remove_silence,
            "enhance_audio": self._op_enhance_audio,
            "add_subtitles": self._op_add_subtitles,
            "add_music": self._op_add_music,
        }
        self.temp_files = []
    
    def process(
        self,
        input_path: str,
        operations: List[Operation],
        output_path: str = None
    ) -> str:
        """Execute video processing pipeline dynamically"""
        current_path = input_path
        
        # Sort by priority
        operations = sorted(operations, key=lambda op: op.priority)
        
        print(f"🎬 Starting pipeline with {len(operations)} operations")
        
        for i, operation in enumerate(operations):
            print(f"  [{i+1}/{len(operations)}] {operation.name}")
            
            op_func = self.operations_map.get(operation.name)
            if not op_func:
                print(f"    ⚠️  Unknown operation: {operation.name}")
                continue
            
            temp_output = tempfile.mktemp(suffix=".mp4")
            self.temp_files.append(temp_output)
            
            try:
                op_func(current_path, temp_output, **operation.params)
                current_path = temp_output
                print(f"    ✅ Completed")
            except Exception as e:
                print(f"    ❌ Error: {e}")
                continue
        
        # Save final output
        if output_path is None:
            output_path = tempfile.mktemp(suffix=".mp4")
        
        shutil.copy2(current_path, output_path)
        self._cleanup()
        
        print("✅ Pipeline completed")
        return output_path
    
    def _op_remove_fillers(self, input_path: str, output_path: str, **kwargs):
        remove_fillers(input_path, output_path)
    
    def _op_remove_silence(self, input_path: str, output_path: str, **kwargs):
        remove_silence(input_path, output_path)
    
    def _op_enhance_audio(self, input_path: str, output_path: str, **kwargs):
        enhance_audio(input_path, output_path)
    
    def _op_add_subtitles(self, input_path: str, output_path: str, **kwargs):
        style = kwargs.get("style", "standard")
        add_subtitles(input_path, output_path, style)
    
    def _op_add_music(self, input_path: str, output_path: str, **kwargs):
        music_path = kwargs.get("music_path")
        volume = kwargs.get("volume", 0.15)
        add_background_music(input_path, output_path, music_path, volume)
    
    def _cleanup(self):
        """Remove temp files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        self.temp_files.clear()