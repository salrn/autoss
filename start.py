import os
import time
from datetime import datetime
import pyautogui
from PIL import Image
from pynput import keyboard
from playsound import playsound

print("██▀▄─██▄─██─▄█─▄─▄─█─▄▄─███─▄▄▄▄█─▄▄▄▄█")
print("██─▀─███─██─████─███─██─███▄▄▄▄─█▄▄▄▄─█")
print("▀▄▄▀▄▄▀▀▄▄▄▄▀▀▀▄▄▄▀▀▄▄▄▄▀▀▀▄▄▄▄▄▀▄▄▄▄▄▀")
print("by ccmirza (v1.0.0) free and open source on github")
time.sleep(1)
print("Press enter to use default on any values asked")

# Ask for screenshot interval
try:
    time.sleep(2.5)
    interval_input = input("Enter screenshot interval in seconds (default is 2, minimum is 0.1): ").strip()
    screenshot_interval = float(interval_input) if interval_input else 2.0
    if screenshot_interval < 0.1: # change for less delay
        print("Interval too low. Using minimum of 0.1 seconds.")
        screenshot_interval = 0.1 # change for less delay
except ValueError:
    print("Invalid input. Using default of 2 seconds.")
    screenshot_interval = 2.0

# Get screen resolution
screen_width, screen_height = pyautogui.size()
print(f"Detected screen resolution: {screen_width}x{screen_height}")

# Ask if user wants to auto-scale the crop size
use_scaled_crop = input("Auto-scale screenshot crop area based on your resolution? (Y/N): ").strip().upper() == 'Y'

# Calculate crop size
base_width, base_height = 640, 640
reference_width = 1920  # 1080p reference width

if use_scaled_crop:
    scale_factor = screen_width / reference_width
    crop_width = int(base_width * scale_factor)
    crop_height = int(base_height * scale_factor)
    print(f"Using scaled crop size: {crop_width}x{crop_height}")
else:
    crop_width, crop_height = base_width, base_height
    print(f"Using default crop size: {crop_width}x{crop_height}")

# Calculate crop position (centered)
left = (screen_width - crop_width) // 2
top = (screen_height - crop_height) // 2

# Setup save directory
folder_name = "Collected"
os.makedirs(folder_name, exist_ok=True)

# Script state
recording = False
stop_program = False
session_count = 0
milestone_interval = 250

# Paths for audio
start_sound = os.path.join(os.getcwd(), "Start.mp3")
end_sound = os.path.join(os.getcwd(), "End.mp3")
milestone_sound = os.path.join(os.getcwd(), "Milestone.mp3")

def get_total_in_folder():
    return len([f for f in os.listdir(folder_name) if f.endswith(".png")])

def toggle_recording():
    global recording
    recording = not recording
    sound = start_sound if recording else end_sound
    try:
        playsound(sound)
    except Exception as e:
        print(f"Error playing sound: {e}")

def on_press(key):
    global stop_program
    try:
        if key == keyboard.Key.page_up:
            toggle_recording()
        elif key == keyboard.Key.esc:
            stop_program = True
    except AttributeError:
        pass

def capture_loop():
    global session_count
    while not stop_program:
        if recording:
            screenshot = pyautogui.screenshot()
            cropped = screenshot.crop((left, top, left + crop_width, top + crop_height))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(folder_name, f"{timestamp}.png")
            cropped.save(filename)
            session_count += 1
            total_in_folder = get_total_in_folder()
            print(f"Saved {filename} | Session: {session_count} | Total in folder: {total_in_folder}")
            
            if session_count % milestone_interval == 0:
                try:
                    playsound(milestone_sound)
                    print("Milestone reached!")
                except Exception as e:
                    print(f"Error playing milestone sound: {e}")
        
        time.sleep(screenshot_interval)

# Start keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Press PageUp to toggle recording. Press Esc to quit.")
capture_loop()
listener.join()
print("Program exited.")
