import os
import requests
import gtts
import speech_recognition as sr
from playsound import playsound
import pyautogui
import pywhatkit

r = sr.Recognizer()
vol_actions = {"monte": "volumeup", "baisse": "volumedown", "coupe": "volumemute"}

def playthis(text, lang='fr'):
    tts = gtts.gTTS(text, lang=lang)
    tts.save("tmp.mp3")
    playsound("tmp.mp3")
    os.system('del tmp.mp3' if os.name=='nt' else 'rm -f tmp.mp3')  

def get_audio():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            # audio_data = r.record(source, duration=4)
            audio_data = r.listen(source)
            # print("Recognizing...")
            text = r.recognize_google(audio_data, language="fr-FR")
            return text
    except Exception as e:
        return ""

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
    text= "".join(order[order.index("cherche")+1:])
    pywhatkit.search(text)

def where_am_i():
    specs = requests.get("https://ipinfo.io/json")
    ville = specs.json()["city"]
    playthis("vous étes a "+ville)

def youtu(order):
    order = order.split()
    text= "".join(order[order.index("joue-moi")+1:])
    pywhatkit.playonyt(text)

def note():
    pyautogui.write(get_audio())

def enregistr():
    pyautogui.hotkey('ctrl', 's')

def blabla(order):
    order = order.split()
    text= "".join(order[order.index("de")+1:])
    text = pywhatkit.info(text, 3, True)
    playthis(text, 'en')

playthis("Bienvenue "+os.getlogin()+" je suis Jarvis votre assistant vocal")

run = True
while run:

    #os.system('cls' if os.name=='nt' else 'clear')

    # print("Listening...")
    behest = get_audio()

    if len(str(behest)) > 1:
        print(behest)
    if ("Jarvis" not in behest):
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
    elif "joue-moi" in behest:
        youtu(behest)
    elif "note" in behest:
        note()
    elif "enregistre" in behest:
        enregistr()
    elif "valide" in behest:
        pyautogui.hotkey('enter')
    elif "son" in behest:
        if behest.split()[1] in vol_actions.keys():
            pyautogui.hotkey(vol_actions[behest.split()[1]])
        else:
            text = "désoler je ne connais que les options " + " ".join(vol_actions.keys())
            print(text)
            playthis(text)
    elif "parle-moi" in behest:
        blabla(behest)

playthis("Au revoir !")