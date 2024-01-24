import pywhatkit
import speech_recognition as sr
from multiprocessing import Array, Process, Lock, Queue, Pool
from time import sleep
import time
import pyttsx3
import os
import datetime
import pyjokes

engine = pyttsx3.init()


def speak(command):
    engine.say(command)
    engine.runAndWait()


r = sr.Recognizer()


def listen(q):
    while True:

        with sr.Microphone() as source1:
            r.adjust_for_ambient_noise(source1, duration=0.2)
            audio1 = r.listen(source1, phrase_time_limit=1)
            with Lock():
                q.put(audio1)


def convert(q1):
    q = Queue()
    p = Process(target=listen, args=(q,))
    p.start()
    sleep(1)
    
    while True:
        audio_data = q.get()
            
        try:
            tex = r.recognize_google(audio_data, language="en-in")
            # print(tex)
            with Lock():
                q1.put(tex)
        except:
            pass


def check_command(command):
    if "ask" in command:
        speak("how are you sir.")
    elif "play" in command:
        song = command.replace("play", "")
        speak("playing" + song)
        pywhatkit.playonyt(song)
    elif "time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        speak(time)
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)
    elif 'who is' or 'what is' or 'where is' or 'when is' or 'information' or 'which is' in command:
        result = pywhatkit.info(command, 3, True)
        speak(result)
        print(result)
    elif "thank" in command:
        speak("its always a pleasure working with you sir")
    else:
        pass


if __name__ == '__main__':
    print("Listening...")
    q1 = Queue()
    listOfCommands = []
    p1 = Process(target=convert, args=(q1,))
    p1.start()

    pool = Pool()

    while True:
        sleep(0.5)
        try:
            command = q1.get()
            print(command)
            listOfCommands.append(command)
            pool.map(check_command, listOfCommands)
            listOfCommands.clear()
            
        except:
            pass
