import speech_recognition as sr
from  multiprocessing import Array,Process,Lock,Queue
from time import sleep
import time
r = sr.Recognizer()

def listen(q):
            
    with sr.Microphone() as source1:
        r.adjust_for_ambient_noise(source1,duration = 0.2)
        while True:
            audio1 = r.listen(source1,phrase_time_limit=1.5)
            with Lock():
                q.put(audio1)
        

def convert(q):
    while True:
        try :
                tex = r.recognize_google(q.get())
                print(tex)
        except :
                pass
               

if __name__ == '__main__':
    q = Queue()

    p1 = Process(target=listen, args =(q,))
    p2 = Process(target=convert, args =(q,))
    print("Listening....")
    p1.start()
    sleep(1)
    p2.start()

    p1.join()
    p2.join()
    
    