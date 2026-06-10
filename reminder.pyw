import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time

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
        target_times = [(21, 30), (21, 31)]  # trigger time
        
        if (current_time.hour, current_time.minute) in target_times:
            result = messagebox.askyesno(
                "Reminder",
                "Richard, your mom is asking you: Do you agree to shut down your PC and go to bed at 10:30pm every night?"
            )
            
            if result:
                print("User agreed to the reminder")
                #root.destroy()
                time.sleep(60)  # Wait 1 minute before continuing
            else:
                print("User declined or closed the reminder, showing again")
                

if __name__ == "__main__":
    show_reminder()
