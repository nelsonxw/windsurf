import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import pyttsx3
import threading

def show_reminder():
    message = "Richard, your mom is asking you ......: Do you agree to shut down your PC and go to bed at 10:30pm every night?"

    def play_voice():
        # Initialize fresh engine for each trigger
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        else:
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
        
        try:
            engine.say(message)
            engine.runAndWait()
        except:
            pass
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    target_times = [(14, 34), (14, 35)]  # trigger time

    while True:
        current_time = datetime.now().time()
        
        if (current_time.hour, current_time.minute) in target_times:
            
            # Start voice in separate thread
            voice_thread = threading.Thread(target=play_voice)
            voice_thread.daemon = True
            voice_thread.start()
            
            # Make window appear on top
            root.attributes('-topmost', True)
            root.lift()
            root.focus_force()
            
            # Show messagebox immediately
            result = messagebox.askyesno(
                "Reminder",
                message
            )
            
            # Reset topmost attribute
            root.attributes('-topmost', False)
            
            if result:
                print("User agreed to the reminder")
                time.sleep(60)  # Wait 1 minute before continuing
            else:
                print("User declined or closed the reminder, showing again")
        
        time.sleep(1)  # Check every second

if __name__ == "__main__":
    show_reminder()
