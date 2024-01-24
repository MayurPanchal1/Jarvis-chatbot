import psutil
import pywhatkit
import speech_recognition as sr
from multiprocessing import Array, Process, Lock, Queue, Pool
from time import sleep
import time
import pyttsx3
import os
import datetime
import pyjokes
import nltk
import python_weather
import asyncio
import playsound
import urllib.request
import webbrowser

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

def startup_msg():
    playsound.playsound('E:\Om(All Data)\PROJECTS\JARVIS\CONTENT\sound files\mainProgramStartup.mp3', True)
    speak("All systems online sir.")
    speak("checking web access")
    speak("internet access established" if connect() else "no internet access established")
    speak("checking other systems ")
    sleep(0.1)
    speak("all systems online and ready")



async def getweather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    # fetch a weather forecast from a city
    weather = await client.find("Pune")

    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)

    # get the weather forecast for a few days
    for forecast in weather.forecasts:
        cast = forecast.sky_text 
        temp = forecast.temperature
        speak(f"Todays expected weather conditions are {cast}")
        speak(f"Todays temperature is {temp}")

        break
    # close the wrapper once done
    await client.close()


engine = pyttsx3.init()

def speak(command):
    playsound.playsound('E:\Om(All Data)\PROJECTS\JARVIS\CONTENT\sound files\Jarvis Startup sound.mp3', True)
    engine.say(command)
    engine.runAndWait()


r = sr.Recognizer()
r1 = sr.Recognizer()

def listen_short():
        with sr.Microphone() as source:
            audio = r1.listen(source)
        try:
            text = r1.recognize_google(audio).lower()
            print(text)
            return text
        except:
            speak("Unable to recognize") 
            return ""        


def listen(q):
            
    with sr.Microphone() as source1:
        r.adjust_for_ambient_noise(source1, duration=0.2)
        while True:
            audio1 = r.listen(source1, phrase_time_limit=1)
            with Lock():
                q.put(audio1)


def convert(q1):
    q = Queue()
    p = Process(target=listen, args=(q,))
    p.start()
    

    while True:
        
        audio_data = q.get()
            
        try:
            tex = r.recognize_google(audio_data, language="en-in").lower()
            # print(tex)
            with Lock():
                q1.put(tex)
            
        except:
            pass 

def find_files(filename, search_path):
   result = ""

# Wlaking top-down from the root
   for root, dir , files in os.walk(search_path):
      if filename in files:
         result +=  os.path.join(root, filename)
   return result

def reminder(t,topic=""):
    speak("your reminder was set.")
    sleep(t*60)
    if topic == "":
        speak("This is a reminder for you ")
        speak("dosent have much informatin")
    else:
        speak(f"This is a reminder for you for {topic}")


# def open_applications():
#     command = listen_short()

#     if "chrome" in command:
#         # os.startfile("C:\Users\Admin\Desktop\short\Google Chrome")
#     elif "whatsapp" in command:
#         webbrowser.open("https://web.whatsapp.com/")
#     elif "telegram" in command:
#         os.startfile("C:\Users\Admin\Desktop\short\Telegram")
#     elif ("computer"or"this pc") in command:
#         os.startfile("C:\Users\Admin\Desktop\short\This PC - Shortcut")
#     elif "control panel" in command:
#         os.startfile("C:\Users\Admin\Desktop\short\Control Panel - Shortcut")
#     elif "youtube" in command:
#         webbrowser.open("youtube.com")
#     elif ("map"or"maps") in command:
#         webbrowser.open("https://www.google.com/maps")
#     elif "mail" in command:
#         webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
#     else:
#         pass



def check_command(command):
    if "jarvis" in command:
        speak("At your service sir")
    

    elif ("music") in command:
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
    elif ("search"or"websearch"or"web") in command:
        command = ""
        speak("can you say whom or what do you want me to search for")
        text = listen_short()
        try :
            result = pywhatkit.info(text, 1, True)
            speak(result)
            print(result)
        except:
            pass

    elif ("notes"or"note") in command:
        command = ""
        text = []
        speak("sir opening notes file")
        f = open("notes.txt","a")
        while True:
            text.append(listen_short())
            speak("Are you done sir")
            ask = listen_short()
            if "yes" in ask:
                break

        for i in text:
            f.write(i)
        f.close()
        speak("sir your notes were saved ")
    
    elif  "file" in command:
        command = ""
        opened = False
        try:
            speak("tell the name of the file you want to open")
            text = listen_short().capitalize()
            print(text)
            os.startfile(f"E:\OM DATA\PYTHON SCRIPTS\Shortcut\{text} - Shortcut")

        except:
            speak("unable to open the specified file")

        

    elif "thank" in command:
        speak("its always a pleasure working with you sir")
    
    # elif ("reminder"or "set") in command:
    #     try:
    #         command = ""
    #         speak("what is the topic of the reminder")
    #         topic = listen_short()
    #         speak("set the time in minutes")
    #         t = listen_short()
    #         for i in t:
    #             if i.isnumeric():
    #                 t = i
    #                 break
    #         t = int(t)
    #         print(t," is the time of the reminder")
    #         p2 = Process(target=listen, args=(t,topic,))
    #         p2.start()

    #     except:
    #         pass
    elif "weather" in command:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(getweather()) 
    
    # elif "open" in command:


    else:
        pass


if __name__ == '__main__':
    q1 = Queue()
    listOfCommands = []
    t = 1
    topic = ""
    p1 = Process(target=convert, args=(q1,))
    # p2 = Process(target=reminder,args=(t,topic,))
    p3 = Process(target=startup_msg)
    p1.start()
    p3.start()


    
    pool = Pool()

    while True:
        try:
            command = q1.get()
            print(command)
            listOfCommands.append(command)
            pool.map(check_command, listOfCommands)
            listOfCommands.clear()
            
        except:
            pass


