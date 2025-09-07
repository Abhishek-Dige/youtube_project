import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 🧠 Narration text
script_dir = os.path.dirname(os.path.abspath(__file__))
narration_path = os.path.join(script_dir, "narration.txt")

with open(narration_path, "r", encoding="utf-8") as f:
    text = f.read()
    print(f"🧠 Narration character count: {len(text)}")
    print(f"🧠 Narration word count: {len(text.split())}")

# 🎤 Voice ID
VOICE_ID = "YXpFCvM1S3JbWEJhoskW"  # Neeraj

# 🔑 Your API keys (rotate if needed)
API_KEYS = [
    os.getenv("V1_KEY"),
    os.getenv("V2_KEY")
]

# 🧾 Voice settings
voice_settings = {
    "stability": 0.4,
    "similarity_boost": 0.8
}

# 🌐 Endpoint
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

# 🔄 Try all keys
for key in API_KEYS:
    print(f"🔁 Trying API key: {key[:10]}...")

    headers = {
        "xi-api-key": key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": voice_settings
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        with open("narration.mp3", "wb") as f:
            f.write(response.content)
        print(f"✅ Success with key {key[:10]} — saved as 'narration.mp3'")
        break
    else:
        print(f"❌ Key {key[:10]} failed with status {response.status_code}")
        try:
            print("  ‣ Error:", response.json())
        except:
            print("  ‣ Raw:", response.text)
else:
    print("🚫 All API keys failed. Please check credits or keys.")
