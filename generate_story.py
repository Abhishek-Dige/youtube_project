import os

import json
import random
import hashlib
import difflib
from datetime import datetime
import pyautogui
import pyperclip
import subprocess
import time
import threading
import keyboard
import tkinter as tk

# === PyAutoGUI Failsafes ===
pyautogui.FAILSAFE = True
stop_flag = False

def sleepcheck(seconds):
    for i in range(seconds):
        if stop_flag:
            print("\n🛑 Script stopped during sleep.")
            exit()
        print(f"⏳ Waiting: {i+1}/{seconds} sec", end="\r")
        time.sleep(1)

# === STOP BUTTON GUI ===
def show_stop_button():
    def stop_script():
        global stop_flag
        stop_flag = True
        print("\n🟥 STOP button clicked.")
        root.destroy()

    root = tk.Tk()
    root.title("STOP Automation")
    root.geometry("200x100+1650+900")
    root.configure(bg="black")
    root.lift()
    root.attributes("-topmost", True)

    stop_btn = tk.Button(root, text="🟥 STOP", font=("Arial", 16, "bold"),
                         fg="white", bg="red", command=stop_script)
    stop_btn.pack(expand=True, fill='both', padx=10, pady=10)

    root.mainloop()

# === ESC LISTENER ===
def esc_listener():
    global stop_flag
    keyboard.wait('esc')
    stop_flag = True
    print("\n❌ ESC pressed.")

threading.Thread(target=show_stop_button, daemon=True).start()
threading.Thread(target=esc_listener, daemon=True).start()

def delete_old_images_by_prompt_count():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    if os.path.exists("prompts.txt"):
        with open("prompts.txt", "r", encoding="utf-8") as f:
            lines = [line for line in f if line.strip()]
            count = len(lines)
        deleted = 0
        for file in sorted(os.listdir(downloads_path)):
            if file.startswith("piclumen") and file.endswith(".png"):
                os.remove(os.path.join(downloads_path, file))
                print(f"🗑️ Deleted previous image: {file}")
                deleted += 1
                if deleted >= count:
                    break

# Run the function before overwriting files
delete_old_images_by_prompt_count()
# === 1. CLEANUP ===
FILES_TO_DELETE = ["final_video.mp4", "final_with_subs.mp4","narration.mp3"]
FILES_TO_OVERWRITE = ["prompts.txt", "narration.txt", "info.json"]

for file in FILES_TO_DELETE:
    if os.path.exists(file):
        os.remove(file)
        print(f"🗑️ Deleted: {file}")

for file in FILES_TO_OVERWRITE:
    with open(file, "w", encoding="utf-8") as f:
        f.write("")
    print(f"📝 Emptied: {file}")

if not os.path.exists("story_db.json"):
    with open("story_db.json", "w", encoding="utf-8") as f:
        json.dump([], f)

# === 2. RANDOM INGREDIENTS ===
import random

branches = [
    "Kids Story",
    "Daily Fact",
    "History Lesson",
    "Urban Legend / Mini Horror",
    "Sci-Fi / Futuristic",
    "Magical Realism / Folklore",
    "Crime Story"
]

branch_config = {
    "Kids Story": {
        "tone": "cheerful, simple, age-appropriate; gentle moral; imaginative language",
        "factual": False
    },
    "Daily Fact": {
        "tone": "concise, curiosity-driven, informative; present verifiable fact(s) with date/place where relevant",
        "factual": True
    },
    "History Lesson": {
        "tone": "documentary, factual, names/dates/places, cause-and-effect context",
        "factual": True
    },
    "Urban Legend / Mini Horror": {
        "tone": "suspenseful, eerie, atmospheric; found-photo vibe allowed; keep non-graphic",
        "factual": False
    },
    "Sci-Fi / Futuristic": {
        "tone": "speculative, vivid, grounded-in-logic if possible",
        "factual": False
    },
    "Magical Realism / Folklore": {
        "tone": "poetic, surreal, grounded in everyday detail",
        "factual": False
    },
    "Crime Story": {
        "tone": "investigative, realistic; include dates/places/names where appropriate; avoid inventing legal outcomes",
        "factual": True
    }
}

branch = random.choice(branches)
cfg = branch_config[branch]

prompt = f"""
You are a professional short-story OR micro-documentary writer for 120-second shorts.
GENERATE ONE piece for branch: {branch}

MUST FOLLOW THESE RULES EXACTLY:

1) LENGTH & FORMAT
- Narration must be a single paragraph of ~250–300 words (spoken time ≈ 120 seconds).
- Output must be EXACTLY in this format, nothing extra:
   Title: (max 12 words)
   Description: (one short YouTube-style blurb, 1–2 lines)
   Narration: (one single paragraph, ~250–300 words)
   Image Prompts: (10–15 standalone scene descriptions, one per line, no numbering)

2) TONE & FACTS
- Tone: {cfg['tone']}.
- If the branch is factual (Daily Fact, History Lesson, Crime Story), include verifiable dates, places, and names when relevant. Use historically reported facts only. If unsure about a specific detail, say "widely reported accounts" rather than inventing specifics.
- If the branch is fictional/fantastical, invent freely but keep imagery vivid and coherent.

3) IMAGE PROMPT RULES (critical — follow exactly)
- Produce 10–15 independent image prompt lines.DO NOT GENERATE OR INCLUDE ANY IMAGES
- Each prompt line must be a standalone scene description (no references like "see above" or pronouns referring to earlier lines).
- Choose up to 3 recurring core objects (for example: "marble statue of a grieving woman", "empty gilt frames", "Isabella Stewart Gardner Museum exterior") if needed — if you introduce a recurring object, **lock its exact adjective+noun phrase** the first time and use that **same exact phrase** whenever that object is referenced again in any later prompt line. (Example: if first reference is "marble statue of a grieving woman", every later reference must be the exact string "marble statue of a grieving woman".)
- Vary camera angle, distance, and secondary details across lines to create contiguous atmosphere (wide shot, close-up, reflection, shadow) while keeping locked phrases stable.
- Do not use pronouns in any image prompt.
- Append these style tokens to the end of every prompt line exactly: "photorealistic, cinematic lighting, 35mm, film grain, ultra-detailed".

4) HOOK & PACING
- Start the Narration with a strong hook sentence (no slow buildup).
- Make the piece emotionally immediate (documentary tone for factual branches; cinematic/poetic for others).
- Keep language natural and crisp; avoid long blown-out exposition.DO NOT INCLUDE ANY HYPERLINKS IN NARRATION.

5) SAFETY & ETHICS
- Do not invent criminal convictions, confessions, or legal outcomes. If speculating about suspects or leads, use neutral phrasing like "investigators suspected" or "reports suggested".
- For real-person mentions, use historical public figures and widely reported facts only.

OUTPUT:
- Return only the numbered fields 1–4 as exact text. No additional commentary, no meta,NO NUMBERING OF TITLE DESCRIPTION ETC .

Generate now for branch: {branch}
""".strip()


pyperclip.copy(prompt)
time.sleep(0.3)

subprocess.Popen([
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--profile-directory=Profile 1",
    "https://chat.openai.com"
])
sleepcheck(7)
pyautogui.click(785, 524)  # Click textbox
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")
sleepcheck(12)  # Wait for response to generate
# 🖼️ Try finding and clicking the "Copy" button visually
copy_img_path = os.path.join(os.path.dirname(__file__), "down_button.png")
print("🖱️ Looking for down button on screen...")

location = pyautogui.locateOnScreen(copy_img_path, confidence=0.8)
if location:
    x, y = pyautogui.center(location)
    pyautogui.moveTo(x, y, duration=0.3)
    for i in range(5):
        pyautogui.click()
        sleepcheck(1)
    
    print("✅ down button clicked!")
else:
    print("❌ Failed to locate down button.")
    exit(1)

sleepcheck(1)
# 🖼️ Try finding and clicking the "Copy" button visually
copy_img_path = os.path.join(os.path.dirname(__file__), "copy_button.png")
print("🖱️ Looking for Copy button on screen...")

location = pyautogui.locateOnScreen(copy_img_path, confidence=0.8)
if location:
    x, y = pyautogui.center(location)
    pyautogui.moveTo(x, y, duration=0.3)
    pyautogui.click()
    print("✅ Copy button clicked!")
else:
    print("❌ Failed to locate Copy button.")
    exit(1)

sleepcheck(1)
pyautogui.hotkey("ctrl", "w")  # Close the browser tab

print("📥 GPT response copied. Proceeding to parse...")

# === 4. Parsing GPT Response ===
def idea_hash(text):
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()

def is_duplicate(new_idea, db, threshold=0.65):
    new_hash = idea_hash(new_idea)
    for entry in db:
        if entry.get("hash") == new_hash:
            return True
        score = difflib.SequenceMatcher(None, new_idea.lower(), entry["idea"].lower()).ratio()
        if score > threshold:
            return True
    return False

def parse_gpt_response(text):
    sections = {"title": "", "description": "", "narration": "", "image_prompts": []}
    lines = text.strip().splitlines()
    mode = None
    for line in lines:
        line = line.strip().lstrip('* ').rstrip('* ').strip()
        if line.lower().startswith("title:"):
            mode = "title"
            sections["title"] = line.split(":", 1)[1].strip().replace("*", "").strip().strip()
        elif line.lower().startswith("description:"):
            mode = "description"
            sections["description"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("narration:"):
            mode = "narration"
            sections["narration"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("image prompts:"):
            mode = "image_prompts"
        elif mode == "image_prompts" and line:
            sections["image_prompts"].append(line.strip())
        elif mode and line:
            sections[mode] += " " + line
    return sections

# === 5. Load DB ===
with open("story_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

response_text = pyperclip.paste()

# === Clipboard Check ===
if response_text.strip() == "" or response_text.strip() == prompt.strip():
    print("❌ Clipboard is empty or still contains the prompt. Aborting.")
    exit(1)

response = parse_gpt_response(response_text)

if is_duplicate(response["narration"], db):
    print("❌ Story is too similar to an existing one. Exiting.")
    exit(1)

# === 6. Save Files ===
info = {
    "title": response["title"],
    "description": response["description"],
    "file_path": os.path.abspath("final_with_subs.mp4")
}
with open("info.json", "w", encoding="utf-8") as f:
    json.dump(info, f, indent=2)

with open("narration.txt", "w", encoding="utf-8") as f:
    f.write(response["narration"].strip())

with open("prompts.txt", "w", encoding="utf-8") as f:
    for prompt in response["image_prompts"]:
        f.write(prompt.strip() + "\n")

# === 7. Update DB ===
db.append({
    "title": response["title"],
    "idea": response["narration"],
    "hash": idea_hash(response["narration"]),
    "created": datetime.now().isoformat()
})
with open("story_db.json", "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2)

print("\n✅ Unique story saved and logged to database.")
