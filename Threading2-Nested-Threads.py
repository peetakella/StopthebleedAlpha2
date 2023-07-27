import logging
import threading
import time

def thread_function1():
    logging.info("Thread 1: starting")
    time.sleep(2)
    logging.info("Thread 1: finishing") #%s inputs name in this case. If you have 2 %s you ned 2 variables and it will show them sequentially



def thread_function2():
    logging.info("Thread 2: starting")
    time.sleep(2)
    z = threading.Thread(target=thread_function3)
    logging.info("Thread 2 : Before thread 3 starts")
    z.start()
    z.join()
    logging.info("Thread 2: finishing") #%s inputs name in this case. If you have 2 %s you ned 2 variables and it will show them sequentially

def thread_function3():
    logging.info("Thread 3: starting")
    time.sleep(2)
    logging.info("Thread 3: finishing") #%s inputs name in this case. If you have 2 %s you ned 2 variables and it will show them sequentially


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
logging.info("Main : before creating thread")
x = threading.Thread(target=thread_function1)
y = threading.Thread(target=thread_function2)    
logging.info("Main : before running thread 1")
x.start()
logging.info("Main : before running thread 2")
y.start()
logging.info("Main : wait for the thread 1 to finish")
x.join()
logging.info("Main : wait for the thread 2 to finish")
y.join()

logging.info("Main : all done")