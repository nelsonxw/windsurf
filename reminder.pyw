import tkinter as tk
from datetime import datetime
import time
import threading
import os
from playsound3 import playsound
from PIL import Image, ImageTk

# Constants
WINDOW_SIZE = "450x450"
GIF_SIZE = (400, 300)
ANIMATION_DELAY = 100
MESSAGE_FONT = ("Arial", 11, "bold")
MESSAGE_COLOR = "red"
BUTTON_WIDTH = 12
BUTTON_FONT = ("Arial", 11, "bold")
YES_BUTTON_COLOR = "#4CAF50"
NO_BUTTON_COLOR = "#f44336"
BUTTON_TEXT_COLOR = "white"
CHECK_INTERVAL = 1
BYPASS_DURATION = 60

# Configuration
REMINDER_TIMES = [(21, 30), (22, 00)] # 9:30 PM and 10:00 PM
FINAL_REMINDER_TIME = (22, 30) # 10:30 PM
SHUTDOWN_TIME = (22, 35) # 10:35 PM

REMINDER_MESSAGE = "Richard, did you agree to shut down your PC and go to bed at 10:30pm every night?"
FINAL_MESSAGE = "Go Sleep Now! Shut down in 5 minutes.  Save all your work!"
REMINDER_VOICE = "Reminder.m4a"
FINAL_VOICE = "Final.m4a"
REMINDER_GIF = "go_to_bed.gif"
FINAL_GIF = "monster.gif"


class AnimatedPopup:
    def __init__(self, parent, gif_path, message, title="Reminder", show_buttons=True):
        self.parent = parent
        self.gif_path = gif_path
        self.message = message
        self.title = title
        self.result = None
        self.show_buttons = show_buttons
        self.gif_frames = []
        self.gif_label = None
        
        self._create_window()
        self._add_message()
        self._load_and_display_gif()
        if self.show_buttons:
            self._add_buttons()
        self._center_window()
        self._ensure_visibility()
    
    def _create_window(self):
        self.popup = tk.Toplevel(self.parent)
        self.popup.title(self.title)
        self.popup.geometry(WINDOW_SIZE)
        self.popup.attributes('-topmost', True)
        self.popup.lift()
        self.popup.focus_force()
        self.popup.transient(self.parent)
        self.popup.grab_set()
        self.popup.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def _add_message(self):
        message_label = tk.Label(
            self.popup,
            text=self.message,
            font=MESSAGE_FONT,
            fg=MESSAGE_COLOR,
            wraplength=430,
            justify=tk.CENTER
        )
        message_label.pack(pady=(15, 10))
    
    def _load_and_display_gif(self):
        self.load_gif()
        
        if self.gif_frames:
            gif_frame = tk.Frame(self.popup)
            gif_frame.pack(pady=(5, 10))
            self.gif_label = tk.Label(gif_frame)
            self.gif_label.pack()
            self.animate_gif(0)
        else:
            tk.Label(self.popup, text="Animation not found", font=("Arial", 12)).pack(pady=(5, 10))
    
    def _add_buttons(self):
        button_frame = tk.Frame(self.popup)
        button_frame.pack(pady=(15, 20), fill=tk.X, padx=20)
        
        yes_btn = tk.Button(
            button_frame,
            text="Yes",
            command=self.on_yes,
            width=BUTTON_WIDTH,
            font=BUTTON_FONT,
            bg=YES_BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            relief=tk.RAISED
        )
        yes_btn.pack(side=tk.LEFT, padx=10, expand=True)
        
        no_btn = tk.Button(
            button_frame,
            text="No",
            command=self.on_no,
            width=BUTTON_WIDTH,
            font=BUTTON_FONT,
            bg=NO_BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            relief=tk.RAISED
        )
        no_btn.pack(side=tk.RIGHT, padx=10, expand=True)
    
    def _center_window(self):
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (self.popup.winfo_width() // 2)
        y = (self.popup.winfo_screenheight() // 2) - (self.popup.winfo_height() // 2)
        self.popup.geometry(f"+{x}+{y}")
    
    def _ensure_visibility(self):
        self.popup.deiconify()
        self.popup.lift()
        self.popup.focus_set()
        self.popup.grab_set()
    
    def load_gif(self):
        try:
            with Image.open(self.gif_path) as img:
                for i in range(img.n_frames):
                    img.seek(i)
                    resized = img.copy().resize(GIF_SIZE, Image.LANCZOS)
                    frame = ImageTk.PhotoImage(resized)
                    self.gif_frames.append(frame)
        except Exception as e:
            pass
    
    def animate_gif(self, frame_index):
        if self.gif_frames:
            self.gif_label.config(image=self.gif_frames[frame_index])
            next_frame = (frame_index + 1) % len(self.gif_frames)
            self.popup.after(ANIMATION_DELAY, self.animate_gif, next_frame)
    
    def on_yes(self):
        self.result = True
        self.popup.destroy()
    
    def on_no(self):
        self.result = False
        self.popup.destroy()
    
    def on_close(self):
        self.result = False
        self.popup.destroy()
    
    def show(self):
        self.popup.wait_window()
        return self.result


def play_voice(audio_file):
    try:
        voice_thread = threading.Thread(target=playsound, args=(audio_file,))
        voice_thread.daemon = True
        voice_thread.start()
    except Exception:
        pass


def is_time_match(current_time, target_time):
    return (current_time.hour, current_time.minute) == target_time


def show_reminder():
    root = tk.Tk()
    root.withdraw()
    
    while True:
        current_time = datetime.now().time()
        
        if is_time_match(current_time, SHUTDOWN_TIME):
            os.system("shutdown /s /t 0")
        
        elif is_time_match(current_time, FINAL_REMINDER_TIME):
            play_voice(FINAL_VOICE)
            popup = AnimatedPopup(root, FINAL_GIF, FINAL_MESSAGE, "Final Reminder", show_buttons=False)
            popup.show()
            time.sleep(BYPASS_DURATION)
        
        elif is_time_match(current_time, REMINDER_TIMES[0]) or is_time_match(current_time, REMINDER_TIMES[1]):
            play_voice(REMINDER_VOICE)
            popup = AnimatedPopup(root, REMINDER_GIF, REMINDER_MESSAGE, "Reminder")
            result = popup.show()
            
            if result:
                time.sleep(BYPASS_DURATION)
        
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    show_reminder()
