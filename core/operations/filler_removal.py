import os
import tempfile
import whisper
from moviepy.editor import VideoFileClip, concatenate_videoclips

FILLERS = ["um", "umm", "uh", "haa", "ah", "er", "hmm", "like", "you know"]

def remove_fillers(video_path: str, output_path: str):
    """Remove filler words using Whisper transcription"""
    print("    🎤 Transcribing and detecting fillers...")
    
    model = whisper.load_model("base")
    video = VideoFileClip(video_path)
    
    # Extract audio
    audio_path = tempfile.mktemp(".wav")
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    
    # Transcribe with timestamps
    result = model.transcribe(audio_path, word_timestamps=True)
    
    # Find filler words
    keep_ranges = []
    last_end = 0.0
    
    for seg in result["segments"]:
        for w in seg.get("words", []):
            word = w["word"].lower().strip()
            if word in FILLERS:
                # Keep segment before filler
                if w["start"] > last_end:
                    keep_ranges.append((last_end, w["start"]))
                last_end = w["end"]
    
    # Keep final segment
    if last_end < video.duration:
        keep_ranges.append((last_end, video.duration))
    
    # Create clips
    clips = [video.subclip(s, e) for s, e in keep_ranges if e - s > 0.25]
    
    if clips:
        final = concatenate_videoclips(clips)
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None
        )
        final.close()
    else:
        # No clips, copy original
        video.write_videofile(output_path, codec="libx264", audio_codec="aac",
                            verbose=False, logger=None)
    
    video.close()
    os.remove(audio_path)