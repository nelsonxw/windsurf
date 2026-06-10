
from playsound3 import playsound
import time

def speak_twice():
    # Play using playsound3 with existing file
    while True:
        playsound("reminder.mp3")
        time.sleep(2)

speak_twice()
