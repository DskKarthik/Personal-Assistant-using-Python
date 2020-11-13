import speech_recognition as sr
import time
import pyttsx3
import wolframalpha
import scrapper

client = wolframalpha.Client('YUWKQG-J5889WW4WV')
engine = pyttsx3.init()
r=sr.Recognizer()

user_dict={
    "wish" : ["hello", "hi", "hai", "hey"] ,
    "leave" : ["bye", "exit", "see you", "shut down"]
}

def take_voice_command():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        input("Press Enter to Activate: ")
        print("Listening...")
        audio=r.listen(source)

        try:
            text=r.recognize_google(audio)
        except:
            text='Sorry I did not get that'
    return text

def respond(cmd):
    
    if "price" in cmd:
        prices,url = scrapper.serch_price(cmd)
        print(url)
        for label,price in prices.items():
            print(label,price,sep=" : ")
        for label,price in prices.items():
            engine.say(label)
            engine.say(price)
            engine.runAndWait()

def transfer_command():
    choice=input("Voice (V) | Text (T). Enter your choice: ")
    if choice.lower() == 'v':
        cmd=take_voice_command()
    else:
        cmd=input("Enter Command Here: ")
    
    return cmd

cmd=transfer_command()
print("[YOU] : ",cmd)
respond(cmd)