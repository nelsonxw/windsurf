
import pyttsx3

engine = pyttsx3.init()
engine.save_to_file("Final Reminder message", "final_reminder.mp3")
engine.runAndWait()
