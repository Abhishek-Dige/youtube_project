import subprocess
import sys

modules = [
    "generate_story.py",
    "image_generation.py",
    "local_tts.py",
    "makevideofinal.py",
    "videowithsubs.py",
    "upload_video.py"
]

print("\n🎬 Starting Full Automation Pipeline...\n")

for i, module in enumerate(modules, 1):
    print(f"[{i}/{len(modules)}] 🚀 Running: {module}")
    result = subprocess.run(["python", module])

    if result.returncode != 0:
        print(f"\n❌ {module} failed. Stopping pipeline.")
        sys.exit(1)
    else:
        print(f"✅ {module} completed successfully.\n")

print("\n🎉 ALL MODULES COMPLETED SUCCESSFULLY 🎉")
