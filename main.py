import re
import speech_recognition as sr
import time
import wolframalpha
import util
import threading
from subprocess import call
import PySimpleGUI as sg
import os

r=sr.Recognizer()

NAME = "Karthik"

def say(text,speak_thread, print_=False):
    if print_:
        l=len(text)

        print('\n== RESULT','='*l)
        print(text)
        print('='*l,'='*10,'\n',sep="")
    
    speak_thread._args=(text,)
    try:
        speak_thread.start()
    except:
        print("Waiting.")
        time.sleep(0.5)
        speak_thread.start()

def speak(phrase):
    call(["python", r"C:\Python Projects\Normal\NLP_Project\speak.py", phrase])


def take_voice_command():
    
    with sr.Microphone() as source:
        # LISTEN FOR AUDIO
        r.adjust_for_ambient_noise(source, duration=0.5)
        input("Press Enter to Activate: ")
        print("Listening...")
        audio=r.listen(source)

        # CONVERT AUDIO (SPEECH) TO TEXT
        try:
            text=r.recognize_google(audio)
        except:
            text='Sorry I did not get that'
        
    return text

def respond(cmd, speak_thread):
    
    # PROCESS THE COMMAND
    
    if re.match("(what|show|tell).*time.*",cmd):
        ctime= time.ctime()
        say(ctime, speak_thread, print_=True)
        return
    
    if re.match(".*open[ ].*", cmd):
        util.open(cmd)
        say(cmd.replace('open','opening'), speak_thread)
        return
    
    if re.match("(.*(tell|say|show).*joke)|([iI].*[ ]bored)", cmd):
        joke = util.get_joke()
        text = "Ok, I got you a joke"+". "+joke
        say(text, speak_thread, print_=True)
        return
    
    if re.match(".*play.*music.*", cmd):
        util.show_songs_list()
        choice = int(input("Select your song (number):"))
        isError = util.play_song(choice)
        if isError:
            print("Please select correct song number..")
            respond("play music",speak_thread)
        return
    
    if re.match(".*stop.*music.*", cmd):
        util.stop_music()
        print("Stopping Music...\n")
        return
    
    if re.match(".*movie|review|imdb.*", cmd.lower()):
        IMBb_url = util.get_IMDb_url(cmd)
        IMDb_summary = util.get_IMDb_summary(IMBb_url)
        say(IMDb_summary,speak_thread)
        return
    
    if re.match('stock|share', cmd.lower()):
        price, change = util.get_stock_price(cmd)
        say(f"Price: {price}. Gain or loss: {change}", speak_thread,print_=True)
        return
    
    if "price" in cmd:
        text = util.search_price(cmd)
        say(text, speak_thread)
        return
    
    if re.match(".*shut([]|[ ])down.*", cmd):
        shutdown = input("Are you sure? (Yes (Y)| No (N))")
        if shutdown:
            os.system("shutdown /s /t 1") 
        return
    
    if util.math_in_cmd(cmd) > 0.33:
        wolfram_res = util.get_wolframalpha_ans(cmd)
        say(wolfram_res, speak_thread, print_=True)
        return
    
    for word in util.user_dict["wish"]:
        if word in cmd:
            say(util.wish()+" "+NAME,speak_thread)
            return

    for word in util.user_dict["leave"]:
        if word in cmd:
            say(util.leave()+ " "+ NAME,speak_thread)
            util.clear_screen()
            exit()
    
    if re.match(".*how are you.*", cmd.lower()):
        say('I am fine', speak_thread)
        return 
    
    if re.match(".*what.*your[ ]name.*", cmd.lower()):
        say("I dont have any name yet. You can call me as your wish and I'll respond", speak_thread)
        return

    # If no match, show a a search page on the query.
    util.search_query(cmd)
    say("Here are few results",speak_thread)

def transfer_command():
    choice=input("Voice (V) | Text (T). Enter your choice: ")
    if choice.lower() == 'v':
        cmd=take_voice_command()
    else:
        cmd=input("Enter Command Here: ")
    
    return cmd

def commandLine():
    while True:
        input("Press Enter to continue. Ctrl+C to exit")
        util.clear_screen()
        cmd=transfer_command()
        util.clear_screen()
        if cmd == "Sorry I did not get that":
            say(cmd)
        else:
            print("[YOU] : ",cmd)
            speak_thread = threading.Thread(target=speak)

            if util.math_in_cmd(cmd) >= 0.33:
                res = util.get_wolframalpha_ans(cmd)
                say(res, speak_thread,print_=True)
            else:
                corrected_text = util.get_corrected_sentence(cmd).lower().strip()
                if corrected_text != cmd:
                    print('Did you mean : "{}" ?'.format(corrected_text))
                    say("Did you mean this?",speak_thread)
                    choice = input("Yes (Y) | No (N) ? :")
                    if choice.lower() in ['yes','y']:
                        cmd = corrected_text
                
                speak_thread = threading.Thread(target=speak)
                #print(speak_thread.is_alive())
                st = time.time()
                respond(cmd, speak_thread)
                et = time.time()
                print("(Result in {} seconds)\n".format(round(et-st,2)))

# ---------- GUI CODE -----------
def start():
    cmd=take_voice_command()
    respond(cmd)

layout = [  [sg.Text('Python Assistant',key='123')],
            [sg.Input(size=(20,5)),sg.Button("OK")],
            [sg.Button("Activate",key='98'), sg.Button("What Can You Do?")] ]

window = sg.Window('Assistant', layout,location=(1300,690))
def GUI():
    while True:
        event, values = window.read()
        if event=='98':
            print('Activated..')
            start()
        if event=="What Can You Do?":
            respond("what can you do")
        if event=="OK":
            respond(values[0])
            values[0]=""
        if event == sg.WIN_CLOSED:
            break


commandLine()