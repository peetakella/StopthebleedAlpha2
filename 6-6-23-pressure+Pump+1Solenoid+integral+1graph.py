#set up digital io
import RPi.GPIO as GPIO          #calling header file which helps us use GPIO’s of PI
GPIO.setwarnings(False)           #do not show any warnings
GPIO.setmode (GPIO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
GPIO.setup(19,GPIO.OUT)       # initialize GPIO19 as an output, not important for the pressure sensor or load cell

#set up graph
import matplotlib.pyplot as plt
plt.figure()
plt.ion()
running_max = 0

#set up i2c
import time
import math
import smbus
from time import sleep
bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
sleep(1)
channel = 1          #select channel

Method = 1 #1 for junction, 2 for tourniquet, 3 for Direct Pressure

#PUL = 17  # Stepper Drive Pulses
PUL = 12  #pwm pin
DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only. 
#
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
#
#print('PUL = GPIO 17 - RPi 3B-Pin #11')
print('DIR = GPIO 27 - RPi 3B-Pin #13')
print('ENA = GPIO 22 - RPi 3B-Pin #15')
print('Initialization Completed')

#Condition sensor for continuous measurements
LOAD_SENSOR_ADDRESS1=0x28
LOAD_SENSOR_ADDRESS2=0x27
LOAD_SENSOR_ADDRESS3=0x26
dummy_command=0x00
offset=1000
#offset=int((input("Enter offset value, default 1000:") or 1000))                                        #subtracts zero offset per data sheet, should be 1000
LOAD_SENSOR_DATA1=bus.read_byte(LOAD_SENSOR_ADDRESS1)#This apparently turns the load sensor on, only need it once
LOAD_SENSOR_DATA2=bus.read_byte(LOAD_SENSOR_ADDRESS2)
LOAD_SENSOR_DATA3=bus.read_byte(LOAD_SENSOR_ADDRESS3)
BLEEDOUT_TIME = 5 #1-6 number being passed through global variable
if BLEEDOUT_TIME == 1:     #3:00
    MAX_MOTOR_SPEED = 14000
if BLEEDOUT_TIME == 2:     #3:30
    MAX_MOTOR_SPEED = 10000
if BLEEDOUT_TIME == 3:     #4:00
    MAX_MOTOR_SPEED = 5500
if BLEEDOUT_TIME == 4:     #4:30
    MAX_MOTOR_SPEED = 4400
if BLEEDOUT_TIME == 5:     #5:00
    MAX_MOTOR_SPEED = 3000
if BLEEDOUT_TIME == 6:     #5:30
    MAX_MOTOR_SPEED = 2500
    
    
global BloodLost
BloodLost = 0


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


global Hz
p=GPIO.PWM(PUL, 100)
GPIO.output(18, 1)     #Open Solenoid
p.start(0)
print('1')
#take continuous measurements and report
L=1
totalsleepcount = 0


global Begin
Begin = 1     #when begin is pressed on GUI, make it = 1



#Junction Wound
while Method == 1 and Begin == 1:
    sleepcount=0
    print('2')
    GPIO.output(18, 1) #Open Solenoid
    p.start(50)
    try :
        bus.write_byte(LOAD_SENSOR_ADDRESS1,dummy_command)#without this command, the status bytes go high on every other read
        LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        print(5)
    except OSError:
        print('Error 1')
        sleep(.1)
        sleepcount += .1
        try :
            LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        except OSError:
            print('Error 2')
            sleep(.1)
            sleepcount += .1
            try :
                LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            except OSError:
                print('Error 3')
                sleep(.1)
                sleepcount += .1
                try :
                    LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    print('Error 4')
                    sleep(.1)
                    sleepcount += .1
                    try :
                        LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        print('Error 5')
                        print('Stopping Motor and Turning off Solenoids')
                        GPIO.output(ENA, GPIO.HIGH)
                        GPIO.output(18, 0)
                        quit()  
    
    sleep(.1)
    sleepcount += .1
    LBS_DATA_SENSOR1=((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
    print ("Sensed load = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000), "pounds")#plots out       
    if LBS_DATA_SENSOR1 < 0:
        LBS_DATA_SENSOR1 = 0
    if LBS_DATA_SENSOR1 > 25 and LBS_DATA_SENSOR1 <= 40:
        LBS_DATA_SENSOR1 = 25
        
    if LBS_DATA_SENSOR1 > 40:
        LBS_DATA_SENSOR1 = 0 
    #sleep(.1) #have seen some status bits activity with delays less than 1 second, most recent experience is that this delay is u
    print('filtered data:',LBS_DATA_SENSOR1, 'Pounds')
    
    #Graph 
    if LBS_DATA_SENSOR1 > running_max:
        running_max = LBS_DATA_SENSOR1
    plt.plot(totalsleepcount,LBS_DATA_SENSOR1,'b.')
    plt.xlim(totalsleepcount-30, totalsleepcount+10)
    plt.ylim(0, running_max + 10)
    plt.pause(0.1) 
     
    GPIO.output(ENA, GPIO.LOW)
    print('ENA set to LOW - Controller Enabled')
    p.ChangeDutyCycle(50)
    input_min = 0
    input_max = 25
    output_min = 100
    output_max = MAX_MOTOR_SPEED
        # Calculate the ratio
    ratio = (output_max - output_min) / (input_max - input_min)
    print('4')
        #print(ratio)
    translated_value = -(LBS_DATA_SENSOR1) * ratio + output_max
        #print(translated_value)
        
        #
    Hz=translated_value
    print(Hz)
    Flow_Rate = 0.2643*math.log(Hz)-1.5221 #Liters per min
    BloodLost= BloodLost + sleepcount * Flow_Rate / 60
    print('BloodLost is:', BloodLost, 'Liters')
    print('sleepcount is', sleepcount, 'seconds')
        
    totalsleepcount = totalsleepcount + sleepcount
    print('totalsleepcount :',totalsleepcount,'secconds')
        
    L+=1
    print('Loopcount =', L)
    
    #Add data to list
    data1.append(totalsleepcount)
    data2.append(BloodLost)
    data3.append(LBS_DATA_SENSOR1)
    
    
    # Save the data to a file
    with open(filename, "w") as file:
        for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{d1}\t{d2}\t{d3}\n")
        
    if BloodLost >= .5: #total blood lost to shut off machine, default is 3 (liters)
        GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
        GPIO.output(18, 0)          #turn off solenoid
        print('You were not fast enough, your patient lost over 3 liters of blood and died')
        quit()
        
         
    GPIO.output(DIR, GPIO.HIGH)
    print('DIR set to LOW - Moving Forward at ' + str(translated_value))
    print('Controller PUL being driven.')   
    p.ChangeFrequency(Hz)            #Update motor speed to new value of Hz                                   
    print('5')


























        
#Tourniquet        
while Method == 2 and Begin == 1:
    sleepcount=0
    print('2')
    GPIO.output(4, 1) #Open Solenoid 2
    p.start(50)
    try :
        bus.write_byte(LOAD_SENSOR_ADDRESS,dummy_command)#without this command, the status bytes go high on every other read
        LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        print(5)
    except OSError:
        print('Error 1')
        sleep(.1)
        sleepcount += .1
        try :
            LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        except OSError:
            print('Error 2')
            sleep(.1)
            sleepcount += .1
            try :
                LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            except OSError:
                print('Error 3')
                sleep(.1)
                sleepcount += .1
                try :
                    LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    print('Error 4')
                    sleep(.1)
                    sleepcount += .1
                    try :
                        LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        print('Error 5')
                        print('Stopping Motor and Turning off Solenoids')
                        GPIO.output(ENA, GPIO.HIGH)
                        GPIO.output(4, 0)
                        quit()  
    sleep(.1)
    sleepcount += .1
    LBS_DATA_SENSOR=((LOAD_SENSOR_DATA[0]&63)*2**8 + LOAD_SENSOR_DATA[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
    print ("Sensed load = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA[0]&63)*2**8 + LOAD_SENSOR_DATA[1] - offset)*100/14000), "pounds")#plots out       
    if LBS_DATA_SENSOR < 0:
        LBS_DATA_SENSOR = 0
    if LBS_DATA_SENSOR > 25 and LBS_DATA_SENSOR <= 40:
        LBS_DATA_SENSOR = 25
        
    if LBS_DATA_SENSOR > 40:
        LBS_DATA_SENSOR = 0 
    #sleep(.1) #have seen some status bits activity with delays less than 1 second, most recent experience is that this delay is u
    print('filtered data:',LBS_DATA_SENSOR, 'Pounds')
    if LBS_DATA_SENSOR > 0:
        
        GPIO.output(ENA, GPIO.LOW)
        print('ENA set to LOW - Controller Enabled')
        p.ChangeDutyCycle(50)
        input_min = 0
        input_max = 25
        output_min = 100
        output_max = MAX_MOTOR_SPEED
        # Calculate the ratio
        ratio = (output_max - output_min) / (input_max - input_min)
        print('4')
        #print(ratio)
        translated_value = -(LBS_DATA_SENSOR) * ratio + output_max
        #print(translated_value)
        
        #
        Hz=translated_value
        print(Hz)
        Flow_Rate = 0.2643*math.log(Hz)-1.5221 #Liters per min
        BloodLost= BloodLost + sleepcount * Flow_Rate / 60
        print('BloodLost is:', BloodLost, 'Liters')
        print('sleepcount is', sleepcount, 'seconds')
        
        L+=1
        print('Loopcount =', L)
        
        if BloodLost >= 3:
            GPIO.output(ENA, GPIO.HIGH)
            GPIO.output(18, 0)
            print('You were not fast enough, your patient lost over 3 liters of blood and died')
            quit()
        
         # pause due to a possible change direction
        GPIO.output(DIR, GPIO.HIGH)
        print('DIR set to LOW - Moving Forward at ' + str(translated_value))
        print('Controller PUL being driven.')   
        p.ChangeFrequency(Hz)                                               
        print('5')
    else:
        GPIO.output(ENA, GPIO.HIGH)
        GPIO.output(4, 0)




























#Direct Pressure
while Method == 3  and Begin == 1:
    sleepcount=0
    print('2')
    GPIO.output(4, 1) #Open Solenoid 2
    p.start(50)
    try :
        bus.write_byte(LOAD_SENSOR_ADDRESS,dummy_command)#without this command, the status bytes go high on every other read
        LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        print(5)
    except OSError:
        print('Error 1')
        sleep(.1)
        sleepcount += .1
        try :
            LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        except OSError:
            print('Error 2')
            sleep(.1)
            sleepcount += .1
            try :
                LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            except OSError:
                print('Error 3')
                sleep(.1)
                sleepcount += .1
                try :
                    LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    print('Error 4')
                    sleep(.1)
                    sleepcount += .1
                    try :
                        LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        print('Error 5')
                        print('Stopping Motor and Turning off Solenoids')
                        GPIO.output(ENA, GPIO.HIGH)
                        GPIO.output(4, 0)
                        quit()  
    sleep(.1)
    sleepcount += .1
    LBS_DATA_SENSOR=((LOAD_SENSOR_DATA[0]&63)*2**8 + LOAD_SENSOR_DATA[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
    print ("Sensed load = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA[0]&63)*2**8 + LOAD_SENSOR_DATA[1] - offset)*100/14000), "pounds")#plots out       
    if LBS_DATA_SENSOR < 0:
        LBS_DATA_SENSOR = 0
    if LBS_DATA_SENSOR > 25 and LBS_DATA_SENSOR <= 40:
        LBS_DATA_SENSOR = 25
        
    if LBS_DATA_SENSOR > 40:
        LBS_DATA_SENSOR = 0 
    #sleep(.1) #have seen some status bits activity with delays less than 1 second, most recent experience is that this delay is u
    print('filtered data:',LBS_DATA_SENSOR, 'Pounds')
    if LBS_DATA_SENSOR > 0:
        
        GPIO.output(ENA, GPIO.LOW)
        print('ENA set to LOW - Controller Enabled')
        p.ChangeDutyCycle(50)
        input_min = 0
        input_max = 25
        output_min = 100
        output_max = MAX_MOTOR_SPEED
        # Calculate the ratio
        ratio = (output_max - output_min) / (input_max - input_min)
        print('4')
        #print(ratio)
        translated_value = -(LBS_DATA_SENSOR) * ratio + output_max
        #print(translated_value)
        
        #
        Hz=translated_value
        print(Hz)
        Flow_Rate = 0.2643*math.log(Hz)-1.5221 #Liters per min
        BloodLost= BloodLost + sleepcount * Flow_Rate / 60
        print('BloodLost is:', BloodLost, 'Liters')
        print('sleepcount is', sleepcount, 'seconds')
        
        L+=1
        print('Loopcount =', L)
        
        if BloodLost >= 3:
            GPIO.output(ENA, GPIO.HIGH)
            GPIO.output(4, 0)
            print('You were not fast enough, your patient lost over 3 liters of blood and died')
            quit()
        
         # pause due to a possible change direction
        GPIO.output(DIR, GPIO.HIGH)
        print('DIR set to LOW - Moving Forward at ' + str(translated_value))
        print('Controller PUL being driven.')   
        p.ChangeFrequency(Hz)                                               
        print('5')
    else:
        GPIO.output(ENA, GPIO.HIGH)
        GPIO.output(4, 0)