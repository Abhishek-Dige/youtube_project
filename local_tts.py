import os
import subprocess

# ----- CONFIG -----
PIPER_PATH = r"C:\Users\HP\Downloads\piper_windows_amd64\piper"
VOICES_FOLDER = os.path.join(PIPER_PATH, "voices")
INPUT_FILE = "narration.txt"
OUTPUT_FILE = "narration.mp3"

# ----- Step 1: List available moods/voices -----
voices = [f for f in os.listdir(VOICES_FOLDER) if f.endswith(".onnx")]

if not voices:
    print("No voices found in:", VOICES_FOLDER)
    exit()

# print("\nAvailable Voices/Moods:")
# for i, voice in enumerate(voices, 1):
#     print(f"{i}. {voice}")

# ----- Step 2: Select mood -----
# choice = input("\nEnter the number of your mood/voice: ")
# try:
#     choice_index = int(choice) - 1
#     if choice_index not in range(len(voices)):
#         raise ValueError
#     selected_voice = voices[choice_index]
# except ValueError:
#     print("Invalid choice!")
#     exit()

voice_path = os.path.join(VOICES_FOLDER, "en-us-ryan-high.onnx")

# ----- Step 3: Check narration.txt -----
if not os.path.exists(INPUT_FILE):
    print(f"'{INPUT_FILE}' not found in current folder:", os.getcwd())
    exit()

# ----- Step 4: Run Piper -----
command = [
    os.path.join(PIPER_PATH, "piper.exe"),
    "--model", voice_path,
    "--output_file", OUTPUT_FILE
]

with open(INPUT_FILE, "r", encoding="utf-8") as infile:
    text = infile.read()

print(f"\nGenerating speech with en-us-ryan-high.onnx...")
process = subprocess.Popen(command, stdin=subprocess.PIPE)
process.communicate(input=text.encode("utf-8"))

print(f"Done! Output saved as '{OUTPUT_FILE}' in {os.getcwd()}")
