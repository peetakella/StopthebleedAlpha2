#!/usr/Local/bin/python
# -*- coding: utf-8 -*-
#TE FX29 load cell sensor
#################################### SET UP DIGITAL IO ####################################
import RPi.GPIO as IO          # calling header file which helps us use GPIO’s of PI, provides local name "IO"
from appJar import gui         # import appJar library
import sys                     # provides acess to variables and functions that interact with the intepreter
from sys import exit           # import exit function (sys.exit() good for production code because the sys module is always available)
import ctypes                  # library that provides c compatible data types
ctypes.CDLL('libX11.so.6').XInitThreads()
IO.setwarnings(False)          # do not show any warnings
IO.setmode (IO.BCM)            # we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
IO.setup(19,IO.OUT)            # initialize GPIO19 as an output, not important for the pressure sensor or load cell

#global takeDataBool            # boolean variable that indicates when data should be taken
global ouputFile               # write sensor data with time to csv file for graph display
global screamStartTime         # timestamp scream audio starts playing (seconds)
#global myFile

#################################### SET UP I2C ####################################
from time import perf_counter # runtime clock
from datetime import datetime # class for formatting date and time
import smbus                  # smbus library allows us to use i2c 
import os                     # portable way of using operating system dependent functionality like writing to a file
from time import sleep
bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL) (serial data and serial clock)

#################################### LOGIC CONTROL FOR MEASUREMENT ####################################
# NEED LED?
from gpiozero import LED # quick way to set up pins
relay = LED(26) 
relay.off()
sleep(1)
relay.on()
sleep(1) # turns led on and off
#screamStartTime = -5    # initially set to scream file length (seconds)

#################################### SET UP PLOT ####################################
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, ion, show, figure 
plt.ion()       # turns on interactive mode (allows for graph editing)
fig = figure()  # intitalizes figure object

#reset = True
print("HEREEEEE")

#################################### SET UP GUI ####################################
# handle button events 
def Execute(button):
    print(button)
    global takeDataBool
    global restart
    
    if button == "Start":
        plt.ion()
        takeDataBool = True
        restart = True
        app.thread(operate)
    if button == "Stop":
        print("Branch to stop taking data")
        takeDataBool = False
        plt.ioff()
        myFile.close()
        #plt.close('all')
        #plt.close(fig)
        #plt.close(1) 
    if button == "Save":
        print("Branch to save data file")
        plt.close('all')
        plt.close()
        plt.close(fig)
        plt.close(1)
        myFile.close()
    if button == "Exit":
        print("Close Program")
        myFile.close()
        os.system("killall omxplayer.bin")
        confirmExit()
        app.stop()
        sys.exit()

###############################################################################################
# Function: confirmExit
# asks user to confirm termination      
def confirmExit():
    print("CONFRIMEXIT()")
    return app.yesNoBox("Confirm Exit", "Are you sure you want to exit the application?")

###############################################################################################
# Function name: operate
# takes sensor data
def operate():
    print("OPERATE")
    global restart
    global myFile
    
    while takeDataBool == True:
        print("You stuck?")
        if restart:
            print("NO")
            fig.canvas.manager.window.move(00,100) # sets figure window location
            fig.set_size_inches(8,3) # sets figure window size
            HEX_27=0x27
            HEX_28=0x28
            startReg=0x00
            LOAD_SENSOR_DATA27=bus.read_byte(HEX_27) #LOAD_SENSOR_DATA27
            LOAD_SENSOR_DATA28=bus.read_byte(HEX_28)
            print("1")
        #This apparently turns the load sensor on, only need it once
            offset27=900 #int(input("Enter offset for 27, default is 1000") or 1000)
            offset28=825 #int(input("Enter offset for 28, default is 1000") or 1000)

        #take continuous measurements and report
            # print(0)
            os.system("omxplayer --no-keys --loop /home/stopthebleed/STB/ducks1-32839.mp3 &")
            now = datetime.now()
            outputFile = now.strftime("/home/stopthebleed/StoptheBleed/GaleProgramFileSaves"+"%H-%M-%S.csv")
            # print(outputFile, 'outputFile')
            myFile = open(outputFile,'w')
            myFile.write('STB data file - '+ outputFile+'\n')
            myFile.write('time (seconds), direct pressure (pounds), tourniquet (pounds)\n')
            measurementStartTime = perf_counter()
            screamStartTime = -5
            print("2")
            restart = False

        # Mask data registers and declare start register (unused)
        print("a")
        bus.write_byte(HEX_27,0x00)                                         
        LOAD_SENSOR_DATA27 = bus.read_i2c_block_data(HEX_27,startReg,2)                                                                                           
        bus.write_byte(HEX_28,0x00)  
        LOAD_SENSOR_DATA28 = bus.read_i2c_block_data(HEX_28,startReg,2)

        # Applies sensor formula to raw data
        sensorT = ((LOAD_SENSOR_DATA27[0]&63)*2**8 + LOAD_SENSOR_DATA27[1] - offset27)*100/14000
        sensorA = ((LOAD_SENSOR_DATA28[0]&63)*2**8 + LOAD_SENSOR_DATA28[1] - offset28)*100/14000
        print("b")
        # Formats pressure data for graphs
        tourniquetPressureLBF = 20 - sensorT
        appliedPressureLBF = 20 - sensorA
        if tourniquetPressureLBF < 0:
            tourniquetPressureLBF = 0
        if appliedPressureLBF < 0:
            appliedPressureLBF = 0
        print("c")
        elapsedRuntime = perf_counter() - measurementStartTime
        myFile.write('{0:.3f}'.format(elapsedRuntime)+","+'{0:.3f}'.format(sensorA)+","+'{0:.3f}'.format(sensorT)+"\n")
        # print('{0:.3f}'.format(elapsedRuntime)+","+'{0:.3f}'.format(sensorA)+","+'{0:.3f}'.format(sensorT)+"\n")
    
        Sensor = ['Applied Pressure','Tourniquet']
        Flow = [appliedPressureLBF,tourniquetPressureLBF]
        screamTimeElapsed = perf_counter() - screamStartTime
        if (((appliedPressureLBF < 10) or (tourniquetPressureLBF < 10)) and (screamTimeElapsed > 5)):
            os.system("omxplayer --no-keys /home/stopthebleed/STB/ducks1-32839.mp3 &")
            screamStartTime = perf_counter()
    
        plt.bar(Sensor, Flow, color='red')
        plt.title('Flow from Sensors')
        plt.xlabel('Sensor')
        plt.ylabel('Flow')
        plt.draw()
        #plt.pause(0.1)
        plt.clf()
        print("STILL IN")
        sleep(.1) 
        continue
    #if takeDataBool == False:
    print("OUT")
    plt.show(block=True)
    plt.close('all')
    return

# create a GUI variable called app
app = gui("Stop the Bleed Simulator", "800x75") 
app.setFont(20)
app.setBg("blue")
app.location=(0,0)
app.setStopFunction(confirmExit)

# add & configure widgets - widgets get a name, to help referencing them later
print("THERE")
app.addLabel("Execute", "")
app.setLabelBg("Execute", "white")
app.setLabelFg("Execute", "black")
app.addButtons(["Start","Stop","Save","Exit"],Execute)

# start the GUI
app.go()