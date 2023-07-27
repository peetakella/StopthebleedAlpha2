import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name) #%s inputs name in this case. If you have 2 %s you ned 2 variables and it will show them sequentially

if __name__ == "__main__": #The if __name__ == "__main__": block is a common Python idiom that allows you to define code that should only be executed when the script is run as the main program, and not when it is imported as a module.
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    y = threading.Thread(target=thread_function, args=(2,))    
    logging.info("Main : before running thread 1")
    x.start()
    logging.info("Main : before running thread 2")
    y.start()
    logging.info("Main : wait for the thread 1 to finish")
    x.join()
    logging.info("Main : wait for the thread 2 to finish")
    y.join()
    logging.info("Main : all done")