import os
import requests
import gtts
import speech_recognition as sr
from playsound import playsound

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
    




playthis("Au revoir !")