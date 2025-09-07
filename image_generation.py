import pyautogui
import time
import keyboard
import sys
import os
import threading
import tkinter as tk
import webbrowser

# -------------------------
# ✅ GLOBAL STOP FLAG
# -------------------------
stop_flag = False

# -------------------------
# 🟥 STOP BUTTON GUI
# -------------------------
def show_stop_button():
    def stop_script():
        global stop_flag
        stop_flag = True
        print("\n🟥 STOP button clicked.")
        root.destroy()

    root = tk.Tk()
    root.title("STOP Automation")
    root.geometry("200x100+1650+900")  # moved to bottom-right corner
    root.configure(bg="black")
    root.lift()
    root.attributes("-topmost", True)

    stop_btn = tk.Button(root, text="🟥 STOP", font=("Arial", 16, "bold"),
                         fg="white", bg="red", command=stop_script)
    stop_btn.pack(expand=True, fill='both', padx=10, pady=10)

    root.mainloop()

# -------------------------
# ⌨️ ESC KEY LISTENER
# -------------------------
def esc_listener():
    global stop_flag
    keyboard.wait('esc')
    stop_flag = True
    print("\n❌ ESC pressed.")

# -------------------------
# 🧠 FAILSAFE AND THREADS
# -------------------------
pyautogui.FAILSAFE = True
threading.Thread(target=show_stop_button, daemon=True).start()
threading.Thread(target=esc_listener, daemon=True).start()

# -------------------------
# 📜 PROMPTS FILE PATH (Hardcoded)
# -------------------------
PROMPTS_PATH = r"C:\Users\HP\OneDrive\Desktop\Youtube\youtube automation\prompts.txt"

if not os.path.exists(PROMPTS_PATH):
    print("❌ prompts.txt not found next to your script/exe!")
    sys.exit(1)

with open(PROMPTS_PATH, 'r', encoding='utf-8') as f:
    prompts = [line.strip() for line in f if line.strip()]

if not prompts:
    print("⚠️ prompts.txt is empty.")
    sys.exit(1)

print(f"✅ Loaded {len(prompts)} prompts. Starting in 5 seconds...")

# Non-blocking delay function
def sleep_check(seconds):
    for _ in range(int(seconds * 10)):
        if stop_flag:
            break
        time.sleep(0.1)

# Wait for pixel change after generation
def wait_for_pixel_change(x, y, timeout=30):
    start_time = time.time()
    original_color = pyautogui.pixel(x, y)
    print(f"👁️ Watching pixel at ({x},{y}) for change from {original_color}...")

    while time.time() - start_time < timeout:
        if stop_flag:
            break
        current_color = pyautogui.pixel(x, y)
        if current_color != original_color:
            print(f"✅ Pixel changed to {current_color}")
            return True
        time.sleep(0.2)

    print("❌ Timeout: Pixel did not change.")
    return False
def capture_image(index, region=(559, 142, 469, 823)):
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    filename = os.path.join(downloads, f"piclumen-{index:03d}.png")
    pyautogui.screenshot(filename, region=region)
    print(f"📸 Saved: {filename}")

sleep_check(5)

# ✅ OPEN WEBSITE FIRST
webbrowser.open("https://piclumen.com/app/image/create")
sleep_check(16)


# -------------------------
# 🔘 COORDINATES TO FILL
# -------------------------
TEXTBOX_POS = (152, 204)

ASPECT_BTN_POS = (290, 666)
SELECT_ASPECT_POS = (163,791)
GENERATE_BTN = (316, 968)
IMAGE_CHECK_POS = (807, 782)
DOWNLOAD_BTN_POS = (1404, 694)
BACK_BTN_POS = (56, 140)

# 👇 Select Aspect Ratio
# pyautogui.click(908,794)
# sleep_check(3)
# pyautogui.click(1879,127)
# sleep_check(3)

pyautogui.click(ASPECT_BTN_POS)
sleep_check(2)
pyautogui.click(SELECT_ASPECT_POS)
sleep_check(2)


# -------------------------
# 🔁 MAIN LOOP
# -------------------------
for i, prompt in enumerate(prompts):
    if stop_flag:
        print("\n🛑 STOPPED before prompt:", i+1)
        break

    print(f"\n🖼️ Generating image {i+1}/{len(prompts)}: {prompt[:60]}...")

    pyautogui.click(TEXTBOX_POS)
    sleep_check(0.5)
    pyautogui.write(prompt, interval=0.035)

    copy_img_path = os.path.join(os.path.dirname(__file__), "enhance_button.png")
    print("🖱️ Looking for enhance button on screen...")

    location = pyautogui.locateOnScreen(copy_img_path, confidence=0.8)
    if location:
        x, y = pyautogui.center(location)
        pyautogui.moveTo(x, y, duration=0.3)
        pyautogui.click()
        print("✅ enhance button clicked!")
    else:
        print("❌ Failed to locate enhance button.")
        exit(1)
    sleep_check(4)

    

    pyautogui.click(GENERATE_BTN)
    sleep_check(1.5)
    print("⏳ Waiting for generation...")
    pyautogui.moveTo(IMAGE_CHECK_POS)
    sleep_check(1)
    wait_for_pixel_change(*IMAGE_CHECK_POS, timeout=40)

    pyautogui.click(IMAGE_CHECK_POS)
    sleep_check(4)
    pyautogui.moveTo(415,648)
    sleep_check(0.5)

    capture_image(i+1)
    sleep_check(1)

    pyautogui.click(BACK_BTN_POS)
    sleep_check(2)

    pyautogui.click(TEXTBOX_POS)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    sleep_check(1.5)

# -------------------------
# ✅ DONE
# -------------------------
if not stop_flag:
   
   pass
else:
    pyautogui.alert("🛑 Automation stopped manually.")
    exit(1)