import speech_recognition as sr
import time
import wolframalpha
import util
import threading
from subprocess import call
import PySimpleGUI as sg
import os

client = wolframalpha.Client('YUWKQG-J5889WW4WV')
r=sr.Recognizer()

NAME = "Karthik"

def say(text,print_=False):
    if print_:
        l=len(text)

        print('\n== RESULT','='*l)
        print(text)
        print('='*l,'='*10,'\n',sep="")
    
    speak_thread._args=(text,)
    try:
        speak_thread.start()
    except:
        time.sleep(500)
        speak_thread.start()

def speak(phrase):
    call(["python", r"C:\Python Projects\Normal\NLP_Project\speak.py", phrase])

speak_thread = threading.Thread(target=speak)

def take_voice_command():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
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
        text = util.search_price(cmd)
        say(text)
        return
    
    if "what is the time" in cmd or "what time is it" in cmd:
        ctime= time.ctime()
        say(ctime,print_=True)
        return
    
    if 'open' in cmd:
        util.open(cmd)
        say(cmd.replace('open','opening'))
        return
    
    if 'joke' in cmd or 'bored' in cmd:
        joke = util.get_joke()
        text = "Ok, I got you a joke"+". "+joke
        say(text, print_=True)
        return
    
    if 'play music' in cmd:
        util.show_songs_list()
        choice = int(input("Select your song (number):"))
        isError = util.play_song(choice)
        if isError:
            print("Please select correct song number..")
            respond("play music")
        return
    
    if 'stop music' in cmd:
        util.stop_music()
        print("Stopping Music...\n")
    
    if 'movie' in cmd or 'review' in cmd or 'imdb' in cmd.lower():
        IMBb_url = util.get_IMDb_url(cmd)
        IMDb_summary = util.get_IMDb_summary(IMBb_url)
        say(IMDb_summary)
        return
    '''
    if util.math_in_cmd(cmd) > 0.25:
        wolfram_res = util.get_wolframalpha_ans(cmd)
        say(wolfram_res, print_=True)'''
    
    for word in util.user_dict["leave"]:
        if word in cmd:
            say(util.leave()+ " "+ NAME)
            util.clear_screen()
            exit()

    util.search_query(cmd)
    say("Here are few results")

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
            if util.math_in_cmd(cmd) > 0.25:
                res = util.get_wolframalpha_ans(cmd)
                say(res, print_=True)
            else:
                corrected_text = util.get_corrected_sentence(cmd).lower().strip()
                if corrected_text != cmd:
                    print('Did you mean : "{}" ?'.format(corrected_text))
                    say("Did you mean this?")
                    choice = input("Yes (Y) | No (N) ? :")
                    if choice.lower() in ['yes','y']:
                        cmd = corrected_text
                
                st = time.time()
                respond(cmd)
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