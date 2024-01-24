import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import os
import webbrowser

listener = sr.Recognizer()
engine = pyttsx3.init()


def talk(text):
    engine.say(text)
    engine.runAndWait()


talk("Hello sir what can i do for you ")


def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "jarvis" in command:
                command = command.replace('jarvis', '')
                return command
            else:
                take_command()
    except:
        pass


def run_jarvis():
    command = take_command()
    if not command:
        take_command()
    else:
        print(command)
        if ("play" in command) or ("song" in command):
            song = command.replace("play", "")
            talk("playing" + song)
            pywhatkit.playonyt(song)
            print(song)

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            talk(time)

        elif 'joke' in command:
            joke = pyjokes.get_joke()
            print(joke)
            talk(joke)

        elif ("google" in command) or ("chrome" in command):
            talk("opening google chrome")
            os.system("start chrome")

        elif "whatsapp" in command:
            talk("opening whatsapp")
            webbrowser.open("https://web.whatsapp.com/")

        elif "microsoft edge" in command:
            talk("opening microsoft edge")
            os.system("start msedge")

        elif "notepad" in command:
            talk("opening notepad")
            os.system("Notepad")

        elif "excel" in command:
            talk("opening microsoft excel")
            os.system("start excel")

        elif ("powerpoint" in command) or ("presentation" in command):
            talk("opening microsoft powerpoint presentation")
            os.system("start powerpnt")

        elif "word" in command:
            talk("opening microsoft word document")
            os.system("start winword")

        elif ('who is' in command) or ('what is' in command) or ('where is' in command) or (
                'when is' in command) or ('information' in command) or ('which is' in command) or (
                "how is" in command):
            result = pywhatkit.info(command, 3, True)
            talk(result)
            print(result)
        else:
            talk('Sorry sir can you repeat again')


while True:
    run_jarvis()
