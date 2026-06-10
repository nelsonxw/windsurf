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
        target_times = [(10, 56), (10, 58)]  # trigger time
        
        if (current_time.hour, current_time.minute) in target_times:
            # Reinitialize engine for each trigger
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'female' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            else:
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)
            
            message = "Richard, your mom is asking you ......: Do you agree to shut down your PC and go to bed at 10:30pm every night?"
            
            # Play voice synchronously
            try:
                engine.say(message)
                engine.runAndWait()
            except:
                pass
            
            # Show messagebox
            result = messagebox.askyesno(
                "Reminder",
                message
            )
            
            if result:
                print("User agreed to the reminder")
                time.sleep(60)  # Wait 1 minute before continuing
            else:
                print("User declined or closed the reminder, showing again")
        
        time.sleep(1)  # Check every second

if __name__ == "__main__":
    show_reminder()
