import os
import requests
import speech_recognition as sr

r = sr.Recognizer()

while True:

    try:
        with sr.Microphone() as source:
            audio_data = r.record(source, duration=3)
            print("Recognizing...")
            text = r.recognize_google(audio_data, language="fr-FR")
            print(text)
    except Exception as e:
        print(e)
    


exit()