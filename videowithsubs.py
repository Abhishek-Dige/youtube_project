from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import whisper_timestamped as whisper
import moviepy.config as mpy_conf
mpy_conf.IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"


# 📄 Use existing audio file for transcription
AUDIO_FILE = "narration.mp3"
VIDEO_FILE = "final_video.mp4"
OUTPUT_FILE = "final_with_subs.mp4"

# 📌 Step 1: Get timestamped transcription (English)
def get_transcribed_text(filename):
    audio = whisper.load_audio(filename)
    model = whisper.load_model("small", device="cpu")
    result = whisper.transcribe(model, audio, language="en")  # 🟢 English forced
    return result

# 🧾 Step 2: Convert words to styled subtitle clips
def get_text_clips(text):
    text_clips_array = []
    segments = text["segments"]
    for segment in segments:
        for word in segment["words"]:
            text_clips_array.append(
                TextClip(
                    word["text"],
                    fontsize=65,
                    stroke_color="black",
                    stroke_width=1,
                    color="white",
                    font="Arial-Bold"
                )
                .set_start(word["start"])
                .set_end(word["end"])
                .set_position("center")  # ✅ Dead center from all sides
            )
    return text_clips_array

# 🎞️ Step 3: Load video, apply subs, export
original_clip = VideoFileClip(VIDEO_FILE)
transcribed_text = get_transcribed_text(AUDIO_FILE)
text_clips = get_text_clips(transcribed_text)
final_video = CompositeVideoClip([original_clip] + text_clips)
final_video.write_videofile(OUTPUT_FILE, codec="libx264", audio_codec="aac")

print("✅ Final video with centered English subtitles saved.")
