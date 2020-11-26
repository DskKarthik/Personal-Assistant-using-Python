import os
import webbrowser
from googlesearch import search
import scrapper
from pyjokes import get_joke
from spellchecker import SpellChecker
import winsound
import random
import wolframalpha

client = wolframalpha.Client('YUWKQG-J5889WW4WV')

programs={
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "jupyter notebook": r"C:\Users\dskk2\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)\Jupyter Notebook (Anaconda3).lnk",
        "notebook": r"C:\Users\dskk2\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)\Jupyter Notebook (Anaconda3).lnk",
        "vs code":r"C:\Users\dskk2\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "code":r"C:\Users\dskk2\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    }

user_dict={
    "wish" : ["hello", "hi", "hai", "hey"] ,
    "leave" : ["bye", "exit", "see you", "shut down"]
}

assistant_dict={
    "wish" : ["hello", "Hi", "hey"],
    "leave": ["see you","I will Miss you", "Have a good day", "have a nice day"]
}

math_words = ['plus', 'minus', 'divide', 'times', 'multiply', 'subract', 
              'derivative', 'integral', 'sin', 'cosine', 'cos', 'secant','sec', 'tan',
              'remainder', 'modulus', 'less than', 'greater than', 'equals']

math_symbols = ['+', '-', '/', '*', '%', '=']

spell = SpellChecker()

def open(cmd):
    l=cmd.split(' ')
    l.remove('open')
    prg=' '.join(l).lower().strip()
    try:
        os.startfile(programs[prg])
    except:
        for i in search(prg, tld='co.in', stop=1):
            url=i
        webbrowser.get().open(url)

def leave():
    return random.choice(assistant_dict["leave"])

def math_in_cmd(cmd):
    split_cmd = cmd.split()
    count=0
    for i in split_cmd:
        if i in math_symbols or i in math_words:
            count+=1
    return count/len(split_cmd)

def get_wolframalpha_ans(cmd):
    res=client.query(cmd)
    wolfram_res=next(res.results).text
    return wolfram_res


def get_IMDb_url(cmd):
    for url in search(cmd, tld='co.in', stop=12):
        if "imdb" in url:
            return url

def search_price(cmd):
    prices,url = scrapper.serch_price(cmd)
    print(url)
    for label,price in prices.items():
        print(label,price,sep=" : ")
    labels = list(prices.keys())
    price = list(prices.values())
    text = labels[0]+" "+ price[0]+". "+ labels[1]+ " "+ price[1]
    return(text)

def clear_screen():
    os.system('cls')

def gen_rand_joke():
    joke = get_joke()
    return joke

def search_query(query):
    webbrowser.get().open("www.google.com/search?q="+query)

def get_corrected_sentence(text):
    corrected_text=""
    for word in text.split(' '):
        corrected_text+=(spell.correction(word)+ " ")
    return corrected_text

def show_songs_list():
    songs = os.listdir(r"C:\Python Projects\Normal\NLP_Project\Music")
    print("List of Songs:")
    i=0
    for song in songs:
        print("{}. {}".format(i+1,song))
        i+=1

def play_song(i):
    lst = os.listdir(r"C:\Python Projects\Normal\NLP_Project\Music")
    if i<1 or i>=len(lst):
        return True
    else:
        song = os.listdir(r"C:\Python Projects\Normal\NLP_Project\Music")[i-1]

    song_path = 'C:\\Python Projects\\Normal\\NLP_Project\\Music\\' + song
    winsound.PlaySound(song_path, winsound.SND_ASYNC)
    return False

def stop_music():
    winsound.PlaySound(None, winsound.SND_ASYNC)

def get_IMDb_summary(url):
    return scrapper.IMDb_Scrapper(url)