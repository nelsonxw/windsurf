import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import pyttsx3
import threading

def show_reminder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    while True:
        current_time = datetime.now().time()
        time_window = tk.Toplevel(root)
        time_window.title("Current Time")
        time_window.geometry("250x100")
        label = tk.Label(time_window, text=f"Current time: {current_time.strftime('%H:%M:%S')}", font=("Arial", 16))
        label.pack(expand=True)
        time_window.after(100, time_window.destroy)  # Close window after 3 seconds
        time_window.update()
        target_times = [(10, 25), (10, 30)]  # trigger time
        
        if (current_time.hour, current_time.minute) in target_times:
            # Initialize text-to-speech engine
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            # Set to female voice (usually index 1 or check for 'female' in voice name)
            for voice in voices:
                if 'female' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            else:
                # Fallback to second voice if no female voice found
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)
            
            message = "Richard, your mom is asking you ......: Do you agree to shut down your PC and go to bed at 10:30pm every night?"
            
            # Function to play voice in background
            def play_voice():
                try:
                    engine.say(message)
                    engine.runAndWait()
                finally:
                    engine.stop()
            
            # Start voice in separate thread
            voice_thread = threading.Thread(target=play_voice)
            voice_thread.daemon = True
            voice_thread.start()
            
            # Wait for voice thread to complete before showing messagebox
            voice_thread.join(timeout=5)
            
            # Show messagebox immediately
            result = messagebox.askyesno(
                "Reminder",
                message
            )
            
            if result:
                print("User agreed to the reminder")
                time.sleep(60)  # Wait 1 minute before continuing
            else:
                print("User declined or closed the reminder, showing again")
                

if __name__ == "__main__":
    show_reminder()
