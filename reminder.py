import tkinter as tk
from tkinter import messagebox

def show_reminder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    result = messagebox.askyesno(
        "Reminder",
        "Your mom is calling: Do you agree to shut down your PC and go to bed at 10:30pm every night?"
    )
    
    if result:
        print("User agreed to the reminder")
    else:
        print("User declined the reminder")
    
    root.destroy()

if __name__ == "__main__":
    show_reminder()
