import sys
import pyttsx3

if __name__=='__main__':
    engine = pyttsx3.init()
    text = str(sys.argv[1])
    engine.say(text)
    engine.runAndWait()