import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import os
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()


def talk(text):
    engine.say(text)
    engine.runAndWait()


while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "jarvis" in command:
                command = command.replace('jarvis', '')
                print(command)
    except:
        pass



