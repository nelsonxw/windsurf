import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
from playsound3 import playsound
import threading
import os

def show_reminder():
    reminder_message = "Richard, your mom is asking you ......: Do you agree to shut down your PC and go to bed at 10:30pm every night?"
    final_message = "Shut down in 5 minutes.  Save all your works to avoid losing them."
    reminder_voice = "reminder.mp3"
    final_voice = "final.mp3"
    
    def play_voice(choice):
        try:
            # Start voice in separate thread
            voice_thread = threading.Thread(target=playsound, args=(choice,))
            voice_thread.daemon = True
            voice_thread.start()

        except:
            pass

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    target_times = [(22, 20), (22, 21)]  # reminder trigger time at 21:30 and 22:00

    while True:
        current_time = datetime.now().time()

        # Shutdown trigger at 22:35
        if (current_time.hour, current_time.minute) == (22, 23):
            os.system("shutdown /s /t 0")
        
        # Final reminder trigger at 22:30
        elif (current_time.hour, current_time.minute) == (22, 22):
            play_voice(final_voice)
                
            # Make window appear on top
            root.attributes('-topmost', True)
            root.lift()
            root.focus_force()
            messagebox.showinfo("Final Reminder", final_message)
                
        # Reminger trigger at 21:30 and 22:00
        elif (current_time.hour, current_time.minute) in target_times:
            play_voice(reminder_voice)
        
            # Make window appear on top
            root.attributes('-topmost', True)
            root.lift()
            root.focus_force()

            # Show messagebox immediately
            result = messagebox.askyesno(
                reminder_message
            )
        
            # Reset topmost attribute
            #root.attributes('-topmost', False)
            
            if result:
                time.sleep(60)  # Wait 1 minute, bypass the trigger time
            else:
                time.sleep(1)  # Check every second
            
            
            

if __name__ == "__main__":
    show_reminder()
