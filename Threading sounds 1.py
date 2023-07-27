import logging
import threading
import time
import vlc
import vcl.ctrl

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
logging.info("Main : before creating thread")

background = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/police-siren-water-cannon-tear-gas-people-coughing-and-protesters-throwing-stones-at-the-police-during-the-chilean-uprising-november-2019-24871.mp3")
moan = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Please Stop_v1.mp3")
playbackground = 0
playmoan = 0
logging.info("variables set to zero")



def thread_function1():
    logging.info("Thread 1: Pre while loop")
    while 1:
        time.sleep(.2)
        if playbackground == 1:
            logging.info("Thread 1: starting")
            time.sleep(.2)
            background.play()
            time.sleep(1)
            vlc-ctrl volume +0.2
            time.sleep(1)
            vlc-ctrl volume +0.2
            time.sleep(1)
            vlc-ctrl volume +0.2
            time.sleep(1)
            vlc-ctrl volume -0.2
            time.sleep(1)
            vlc-ctrl volume -0.2
            time.sleep(1)
            vlc-ctrl volume -0.2
            time.sleep(1)
            vlc-ctrl volume +0.2
            time.sleep(1)
            vlc-ctrl volume +0.2
            time.sleep(1)
            vlc-ctrl volume +0.2
            time.sleep(1)
            vlc-ctrl volume -0.2
            time.sleep(1)
            vlc-ctrl volume -0.2
            time.sleep(1)
            vlc-ctrl volume -0.2             
            logging.info("Thread 1: finishing") #%s inputs name in this case. If you have 2 %s you ned 2 variables and it will show them sequentially



def thread_function2():
    x = 0
    logging.info("Thread 2: starting")
    time.sleep(.2)
    while 1:
        print("x = ", x)
        logging.info("Thread 2: in the while loop")
        print("playmoan = " , playmoan)
        time.sleep(.2)
        if (playmoan == 1) & (x <= 2): 
            print("playmoan = " ,playmoan)
            moan.play()
            logging.info("Thread 2: Moan played")
            time.sleep(2)
            moan.stop()
            x += 1
            print("x = ", x)
            


   

x = threading.Thread(target=thread_function1)
y = threading.Thread(target=thread_function2)    
logging.info("Main : before running thread 1")
x.start()
logging.info("Main : before running thread 2")
y.start()
time.sleep(5)
playbackground = 1
time.sleep(10)
#playmoan = 1
logging.info("Main : pmaymoan set to 1")

