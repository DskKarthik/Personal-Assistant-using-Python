import speech_recognition as sr
import pyttsx3
import threading

engine = pyttsx3.init()
r=sr.Recognizer()

def callback(r,audio):
    text = r.recognize_google(audio)
    print(text)

def listen():

    with sr.Microphone() as source:

        audio = r.listen(source, snowboy_configuration="google")
        text = r.recognize_google(audio)
        print(text)

listen()