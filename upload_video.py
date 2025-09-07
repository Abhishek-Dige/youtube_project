import pyautogui
import time
import subprocess
import json
import keyboard
import threading
import tkinter as tk

# === 🧠 FAILSAFE SYSTEM ===
stop_flag = False
pyautogui.FAILSAFE = True

def show_stop_button():
    def stop_script():
        global stop_flag
        stop_flag = True
        print("\n🟥 STOP button clicked.")
        root.destroy()

    root = tk.Tk()
    root.title("STOP Upload")
    root.geometry("200x100+1650+900")
    root.configure(bg="black")
    root.lift()
    root.attributes("-topmost", True)

    stop_btn = tk.Button(root, text="🟥 STOP", font=("Arial", 16, "bold"),
                         fg="white", bg="red", command=stop_script)
    stop_btn.pack(expand=True, fill='both', padx=10, pady=10)

    root.mainloop()

def esc_listener():
    global stop_flag
    keyboard.wait('esc')
    stop_flag = True
    print("\n❌ ESC pressed.")

def sleep_check(seconds):
    for _ in range(int(seconds * 10)):
        if stop_flag:
            print("🛑 Sleep interrupted.")
            break
        time.sleep(0.1)

threading.Thread(target=show_stop_button, daemon=True).start()
threading.Thread(target=esc_listener, daemon=True).start()

# === Load video info from JSON ===
with open("info.json", "r", encoding="utf-8") as f:
    info = json.load(f)

title = info["title"]
description = info["description"]
file_path = info["file_path"]

# === Step 1: Open YouTube Upload Page ===
subprocess.Popen([
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--profile-directory=Profile 1",
    "https://www.youtube.com/upload"
])

sleep_check(10)

# === Step 2: Click "Select Files" button ===
pyautogui.click(948, 701)
sleep_check(2)

# === Step 3: Type file path and press Enter ===
pyautogui.write(file_path)
pyautogui.press("enter")
sleep_check(10)

# === Step 4: Ctrl+A, Delete, and type title ===
pyautogui.hotkey("ctrl", "a")
pyautogui.press("backspace")
pyautogui.write(title)
sleep_check(1)

# === Step 5: Click description box and type ===
pyautogui.click(633, 731)
pyautogui.write(description)
sleep_check(1)

# === Step 6: Click "No, it's not made for kids" twice ===
pyautogui.click(1550, 808)
pyautogui.click(1550, 808)
sleep_check(1)

# === Step 7: Click near scrollbar to scroll page ===
pyautogui.click(434, 629)
sleep_check(0.5)

# === Step 8: Click "Next" three times ===
for _ in range(3):
    pyautogui.click(1498, 919)
    sleep_check(0.1)

# === Step 9: Click "Public" option ===
pyautogui.click(497, 675)
sleep_check(1)

# === Step 10: Click "Publish" ===
pyautogui.click(1495, 906)
sleep_check(6)

# === Close the tab (Ctrl + W) ===
pyautogui.hotkey('ctrl', 'w')
sleep_check(1)

if not stop_flag:
    pass
else:
    pyautogui.alert("🛑 Upload Interrupted.")
