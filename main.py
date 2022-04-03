import os
import requests
import gtts
import speech_recognition as sr
from playsound import playsound
import pyautogui

r = sr.Recognizer()

def playthis(text):
    tts = gtts.gTTS(text, lang='fr')
    tts.save("tmp.mp3")
    playsound("tmp.mp3")
    os.system('del tmp.mp3' if os.name=='nt' else 'rm -f tmp.mp3')

def get_audio():
    try:
        with sr.Microphone() as source:
            audio_data = r.record(source, duration=4)
            # print("Recognizing...")
            text = r.recognize_google(audio_data, language="fr-FR")
            return text
    except Exception as e:
        return e

def weather():
    specs = requests.get("https://ipinfo.io/json")
    ville = specs.json()["city"]
    meteo = requests.get("https://prevision-meteo.ch/services/json/"+ville)
    text = "Aujourd'hui il fait "+meteo.json()["fcst_day_0"]["condition"] \
    +" demain la journée sera "+meteo.json()["fcst_day_1"]["condition"]+'\n' \

    print(text)
    playthis(text)

def when():
    raw = requests.get("http://worldtimeapi.org/api/timezone/Europe/Paris")
    datetime = raw.json()["datetime"][:-13]
    tmp = list(datetime)
    for i in [4,7,10,13,16]:
        tmp[i] = ' '
    tmp = ("".join(tmp)).split()
    print(datetime)
    text = "nous sommes le "+tmp[2]+" "+tmp[1]+" "+tmp[0] \
    + " il est" +tmp[3]+" heures "+tmp[4]+" minutes et "+tmp[5]+" secondes"
    playthis(text)

def search(order):
    order = order.split()
    text = "firefox"
    if os.name=='nt':
        text+= ".exe"
    text+= " https://www.google.com/search?q="+"+".join(order[order.index("cherche")+1:])
    os.system(text)

def where_am_i():
    specs = requests.get("https://ipinfo.io/json")
    ville = specs.json()["city"]
    playthis("vous étes a "+ville)

playthis("Bienvenue "+os.getlogin()+" je suis Jarvis votre assistant vocal")

run = True
while run:

    #os.system('cls' if os.name=='nt' else 'clear')

    # print("Listening...")
    behest = get_audio()
    print(behest)

    if len(str(behest)) < 1 or ("Jarvis" not in behest):
        pass
    elif "déconnexion" in behest:
        run = False
    elif ("météo" in behest) or ("temps" in behest):
        weather()
    elif "heure" in behest:
        when()
    elif "cherche" in behest:
        search(behest)
    elif "où suis-je" in behest:
        where_am_i()


playthis("Au revoir !")