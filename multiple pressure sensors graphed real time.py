#TE FX29 load cell sensor

#set up digital io
import matplotlib.pyplot as plt
import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
IO.setwarnings(False)           #do not show any warnings
IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
IO.setup(19,IO.OUT)           # initialize GPIO19 as an output, not important for the pressure sensor or load cell



#set up i2c
import time
import smbus
from time import sleep
bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
channel = 1          #select channel
t=0

#name file to save data to
name = input ("enter trial run name")
filename=(f"{name}.txt")
#Throw error codes for when and if there is something that can't be in a file name and have them try again
print (filename)
#Create empty lists
data1 = []
data2 = []
data3 = []
data4 = []

plt.figure()
plt.ion()
#Condition sensor for continuous measurements
LOAD_SENSOR_ADDRESS1=0x28
LOAD_SENSOR_ADDRESS2=0x27
dummy_command=0x00
offset=1100
#offset=int((input("Enter offset value, default 1000:") or 1000))                                        #subtracts zero offset per data sheet, should be 1000
LOAD_SENSOR_DATA1=bus.read_byte(LOAD_SENSOR_ADDRESS1)#This apparently turns the load sensor on, only need it once
LOAD_SENSOR_DATA2=bus.read_byte(LOAD_SENSOR_ADDRESS2)
running_max = 0

#take continuous measurements and report
while 1:
    
    bus.write_byte(LOAD_SENSOR_ADDRESS1,dummy_command)                                          #without this command, the status bytes go high on every other read
    LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
    LBS_DATA_SENSOR1=((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000                                                                                  #It does return the correct two bytes after the initial read byte command    
    
    bus.write_byte(LOAD_SENSOR_ADDRESS2,dummy_command)                                          #without this command, the status bytes go high on every other read
    LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
    LBS_DATA_SENSOR2=((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000
    
    
    if LBS_DATA_SENSOR1 > running_max:
        running_max = LBS_DATA_SENSOR1
    if LBS_DATA_SENSOR2 > running_max:
        running_max = LBS_DATA_SENSOR2    

    plt.plot(t,LBS_DATA_SENSOR1,'b.')
    plt.plot(t,LBS_DATA_SENSOR2,'r.')
    plt.xlim(t-30, t+10)
    plt.ylim(0, running_max + 10)
    plt.pause(0.1)
    
    #Add data to list
    data1.append(t)
    data2.append(LBS_DATA_SENSOR1)
    data3.append(LBS_DATA_SENSOR2)
    
    
    # Save the data to a file
    with open(filename, "w") as file:
        for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{d1}\t{d2}\t{d3}\n")
    
    #sleep(.1) #have seen some status bits activity with delays less than 1 second, most recent experience is that this delay is u
    t += .2