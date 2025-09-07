import os
import glob
import random
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips, vfx, CompositeAudioClip
import PIL.Image

# Fix for newer versions of Pillow
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

# Paths
downloads_path = r"C:\Users\HP\Downloads"
working_dir = os.getcwd()
prompts_file = os.path.join(working_dir, "prompts.txt")
audio_path = os.path.join(working_dir, "narration.mp3")

# 🎵 Background music
bgm_list = [
    os.path.join(working_dir, "Accept-The-Challenge-chosic.com_.mp3"),
    # os.path.join(working_dir, "another_bgm.mp3"),  # Add more as needed
]
bgm_path = random.choice(bgm_list)  # 🎲 Select random BGM (only one now)

# Get number of lines in prompts.txt
with open(prompts_file, "r", encoding='utf-8') as f:
    num_images = sum(1 for line in f if line.strip())

# Get latest images from Downloads
image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(os.path.join(downloads_path, ext)))
image_files.sort(key=os.path.getmtime, reverse=True)
selected_images = list(reversed(image_files[:num_images]))

# Get audio duration
voiceover_clip = AudioFileClip(audio_path)
total_duration = voiceover_clip.duration
image_duration = total_duration / num_images
print(f"🎧 narration.mp3 duration: {total_duration:.2f} seconds")

# Resize to first image’s size
base_clip = ImageClip(selected_images[0])
target_size = base_clip.size

image_clips = []
for img_path in selected_images:
    try:
        clip = (
            ImageClip(img_path)
            .resize(newsize=target_size)
            .set_duration(image_duration)
            .fadein(0.5)
            .fadeout(0.5)
            .fx(vfx.resize, lambda t: 1 + 0.02 * t)  # slow zoom in
        )
        image_clips.append(clip)
    except Exception as e:
        print(f"⚠️ Skipping {img_path}: {e}")

# 🔊 Layer voice + bgm
bgm_clip = AudioFileClip(bgm_path).volumex(0.08)  # Low background music
final_audio = CompositeAudioClip([voiceover_clip, bgm_clip.set_duration(voiceover_clip.duration)])

# 🎞️ Merge and export
final_clip = concatenate_videoclips(image_clips, method="compose").set_audio(final_audio)
output_path = os.path.join(working_dir, "final_video.mp4")
final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)

print(f"✅ Done! Saved to: {output_path}")
