
import pyttsx3

engine = pyttsx3.init()
engine.save_to_file("Reminder message", "reminder.mp3")
engine.runAndWait()
