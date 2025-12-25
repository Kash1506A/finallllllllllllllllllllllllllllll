# test_music.py
import os

music_dir = "assets/music"
required_files = ["upbeat.mp3", "calm.mp3", "dramatic.mp3", "default.mp3"]

print("🎵 Checking music files...")
print("=" * 50)

for filename in required_files:
    filepath = os.path.join(music_dir, filename)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath) / 1024  # KB
        print(f"✅ {filename:<20} ({size:.1f} KB)")
    else:
        print(f"❌ {filename:<20} MISSING")

print("=" * 50)

if all(os.path.exists(os.path.join(music_dir, f)) for f in required_files):
    print("✅ All required music files present!")
else:
    print("⚠️  Some music files missing. Download from:")
    print("   - YouTube Audio Library: https://www.youtube.com/audiolibrary")
    print("   - Pixabay: https://pixabay.com/music/")