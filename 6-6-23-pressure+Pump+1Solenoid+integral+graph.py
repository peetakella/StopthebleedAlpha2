#set up i2c
import time
tic0 = time.perf_counter()
import math
import smbus
from time import sleep
bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
sleep(1)
channel = 1          #select channel

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
upthreshold1 = 20
plt.axhline(y=20, color='r', linestyle='-', linewidth = 2)

#Variables from GUI
method = 1 #1 for junction, 2 for tourniquet, 3 for Direct Pressure
global begin
begin = 1     #when begin is pressed on GUI, make it = 1
BLEEDOUT_TIME = 1 #1-6 number being passed through global variable (speed in gui)


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
GPIO.setup(4, GPIO.OUT)
#
print('Initialization Completed')

#Condition sensor for continuous measurements
LOAD_SENSOR_ADDRESS1=0x28 #junction
LOAD_SENSOR_ADDRESS2=0x27 #Higher arm sensor
LOAD_SENSOR_ADDRESS3=0x26 #Lower arm sensor
dummy_command=0x00
offset=1000
#offset=int((input("Enter offset value, default 1000:") or 1000))                                        #subtracts zero offset per data sheet, should be 1000
LOAD_SENSOR_DATA1=bus.read_byte(LOAD_SENSOR_ADDRESS1)#This apparently turns the load sensor on, only need it once
#LOAD_SENSOR_DATA2=bus.read_byte(LOAD_SENSOR_ADDRESS2)
#LOAD_SENSOR_DATA3=bus.read_byte(LOAD_SENSOR_ADDRESS3)

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
#Motor speed value is set
input_min = 0
input_max = upthreshold1
output_min = 100 #frequency in hz, higher is faster pumping
output_max = MAX_MOTOR_SPEED
# Calculate the ratio
ratio = (output_max - output_min) / (input_max - input_min)
#print(ratio)
    
global BloodLost
BloodLost = 0

#---------------------------------------------------
#name file to save data to
#name = input ("enter trial run name")
#filename=(f"{name}.txt")
filename = (f"trial.txt")
#Throw error codes for when and if there is something that can't be in a file name and have them try again
print (filename)
#Create empty lists
data1 = []
data2 = []
data3 = []
data4 = []
#---------------------------------------------------

global Hz
p=GPIO.PWM(PUL, 100)   #PWM Function is defined
#GPIO.output(18, 1)     #Open Solenoid
p.start(0)             #PWM is activated at a duty cycle of 0

#Set loop count variable
L=1


tic3 = 0 #timestamp

global totaltime
totaltime = 0

print('1')

cycletime = 0
tic1 = time.perf_counter()














#Junction Wound
while method == 1 :
    #time stamp is taken
    tic2 = time.perf_counter()
    print('2')
    
#---------------------------------------
    #Collect Data, if error happens continue until there are 5 errors in a row then quit
    try :
        bus.write_byte(LOAD_SENSOR_ADDRESS1,dummy_command)#without this command, the status bytes go high on every other read
        LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        print(3)
    except OSError:
        print('Error 1')
        sleep(.1)
        
        try :
            LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        except OSError:
            print('Error 2')
            sleep(.1)
            
            try :
                LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            except OSError:
                print('Error 3')
                sleep(.1)
        
                try :
                    LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    print('Error 4')
                    sleep(.1)
                    
                    try :
                        LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        print('Error 5')
                        print('Stopping Motor and Turning off Solenoids')
                        GPIO.output(ENA, GPIO.HIGH) #stop motor
                        GPIO.output(18, 0) 
                        quit()  
 #---------------------------------------
        #Raw Data is turned into lbs and filtered
    LBS_DATA_SENSOR1=((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
    print ("Sensed load = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000), "pounds")#plots out       
    if LBS_DATA_SENSOR1 < 0:
        LBS_DATA_SENSOR1 = 0
    if LBS_DATA_SENSOR1 > 0 and LBS_DATA_SENSOR1 <= upthreshold1:    
        STB_timer=0
    if LBS_DATA_SENSOR1 > upthreshold1 and LBS_DATA_SENSOR1 <= 40:
        LBS_DATA_SENSOR1 = upthreshold1
        STB_timer = STB_timer + cycletime
        if STB_timer >= 6:#how to actually stop the bleed
            print('You Stopped The Bleed!!!')
            GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
            GPIO.output(18, 0)
            quit()
        
    if LBS_DATA_SENSOR1 > 40:
        LBS_DATA_SENSOR1 = 0 
    print('filtered data:',LBS_DATA_SENSOR1, 'Pounds')
#---------------------------------------
    Hz = -(LBS_DATA_SENSOR1) * ratio + output_max
    print(Hz)
#---------------------------------------
    #Motor is Enabled and frequency is set
    p.start(50) #PWM function is set to duty cycle of 50
    GPIO.output(ENA, GPIO.LOW)  #enable motor
    print('ENA set to LOW - Controller Enabled')
    GPIO.output(DIR, GPIO.HIGH)      #set Directin to CCW   
    p.ChangeFrequency(Hz)            #Update motor speed to new value of Hz
    p.ChangeDutyCycle(50)
#---------------------------------------      
    #time keeping, time start and measured against when motor settings are changed
    tic4 = tic3
    print('tic4=',tic4)
    tic3 = time.perf_counter()
    print('tic3=',tic3)
    if tic4 == 0:
        tic4 = tic3 - .3
        print('tic4=',tic4)
    cycletime = tic3 - tic4
    print ('cycletime =:',cycletime, 'seconds')
#---------------------------------------     

    #Count the times through the loop
    L+=1
    print('Loopcount =', L)
    
#---------------------------------------
    #Calculate Blood Loss
    Flow_Rate = 0.2643*math.log(Hz)-1.5221 #Liters per min
    BloodLost= BloodLost + (cycletime * Flow_Rate / 60)
    print('BloodLost is:', BloodLost, 'Liters')
  
    if BloodLost >= 3: #total blood lost to shut off machine, default is 3 (liters)
        GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
        GPIO.output(18, 0)          #turn off solenoid
        print('You were not fast enough, your patient lost over 3 liters of blood and died')
        quit()
#---------------------------------------
        #Add Progress bar with bloodlost data
#---------------------------------------   
    #Add data to lists
    data1.append(totaltime)
    data2.append(BloodLost)
    data3.append(LBS_DATA_SENSOR1)
    # Save the data to a file
    with open(filename, "w") as file:
        for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{d1}\t{d2}\t{d3}\n")
#---------------------------------------            
    #Update Graph
    if LBS_DATA_SENSOR1 > running_max:
        running_max = LBS_DATA_SENSOR1
    plt.plot(data1,data3,'b-', linewidth=2)
    plt.xlim(0, totaltime+15)
    plt.ylim(0, running_max + 10)
    plt.pause(0.1)
#---------------------------------------       
    #time refrence at the end of the cycle
    tic5 = time.perf_counter()
    totaltime = tic5-tic1
    print (totaltime)
#---------------------------------------     

    #Count the times through the loop
    L+=1
    print('Loopcount =', L)
#---------------------------------------   



















#Tourniquet
while method == 2 :
    #time stamp is taken
    tic2 = time.perf_counter()
    print('2')
    
#---------------------------------------
    #Collect Data, if error happens continue until there are 5 errors in a row then quit
    try :
        bus.write_byte(LOAD_SENSOR_ADDRESS2,dummy_command)#without this command, the status bytes go high on every other read
        bus.write_byte(LOAD_SENSOR_ADDRESS3,dummy_command)#without this command, the status bytes go high on every other read
        LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)
        print(3)
    except OSError:
        print('Error 1')
        sleep(.1)
        
        try :
            LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)
        except OSError:
            print('Error 2')
            sleep(.1)
            
            try :
                LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)  
            except OSError:
                print('Error 3')
                sleep(.1)
        
                try :
                    LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)  
                except OSError:
                    print('Error 4')
                    sleep(.1)
                    
                    try :
                        LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                        LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)
                    except OSError:
                        print('Error 5')
                        print('Stopping Motor and Turning off Solenoids')
                        GPIO.output(ENA, GPIO.HIGH)
                        GPIO.output(4, 0)
                        quit()  
 #---------------------------------------
        #Raw Data is turned into lbs and filtered
    LBS_DATA_SENSOR2=((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
    print ("Sensed load2 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000), "pounds")#plots out
    LBS_DATA_SENSOR3=((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
    print ("Sensed load3 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000), "pounds")#plots out
    
    TOTAL_LBS=LBS_DATA_SENSOR2+LBS_DATA_SENSOR3
 
      #Ratio of load cell data to calcualte where the weight is
    
    distribution = LBS_DATA_SENSOR2/(LBS_DATA_SENSOR2+LBS_DATA_SENSOR3)
    if distribution  < .5:
        print('Apply Tourniquet higher on arm')
 
    if TOTAL_LBS < 0:
        TOTAL_LBS = 0
        TOTAL_LBS_FILTERED = 0
    if TOTAL_LBS > 0 and TOTAL_LBS <= upthreshold1:    
        TOTAL_LBS_FILTERED = TOTAL_LBS
        STB_timer=0
    if TOTAL_LBS > upthreshold1 and TOTAL_LBS <= 40:
        TOTAL_LBS_FILTERED = upthreshold1
        if distribution > .5:
            STB_timer = STB_timer + cycletime
            if STB_timer >= 6:
                print('You Stopped The Bleed!!!')
                GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
                GPIO.output(4, 0)
                quit()
        
    if TOTAL_LBS > 40:
        TOTAL_LBS_FILTERED = 0 
    print('filtered data:',TOTAL_LBS_FILTERED, 'Pounds')
    
#---------------------------------------

    
    
    
    
    
    
#---------------------------------------
    Hz = -(TOTAL_LBS_FILTERED) * ratio + output_max
    print(Hz)
#---------------------------------------
    #Motor is Enabled and frequency is set
    p.start(50) #PWM function is set to duty cycle of 50
    GPIO.output(ENA, GPIO.LOW)
    print('ENA set to LOW - Controller Enabled')
    GPIO.output(DIR, GPIO.HIGH)      #set Directin to CCW   
    p.ChangeFrequency(Hz)            #Update motor speed to new value of Hz
    p.ChangeDutyCycle(50)
#---------------------------------------      
    #time keeping, time start and measured against when motor settings are changed
    tic4 = tic3
    print('tic4=',tic4)
    tic3 = time.perf_counter()
    print('tic3=',tic3)
    if tic4 == 0:
        tic4 = tic3 - .3
        print('tic4=',tic4)
    cycletime = tic3 - tic4
    print ('cycletime =:',cycletime, 'seconds')
#---------------------------------------     

    #Count the times through the loop
    L+=1
    print('Loopcount =', L)
    
#---------------------------------------
    #Calculate Blood Loss
    Flow_Rate = 0.2643*math.log(Hz)-1.5221 #Liters per min
    BloodLost= BloodLost + (cycletime * Flow_Rate / 60)
    print('BloodLost is:', BloodLost, 'Liters')
  
    if BloodLost >= 3: #total blood lost to shut off machine, default is 3 (liters)
        GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
        GPIO.output(4, 0)          #turn off solenoid
        print('You were not fast enough, your patient lost over 3 liters of blood and died')
        quit()
#---------------------------------------
        #Add Progress bar with bloodlost data
#---------------------------------------   
    #Add data to lists
    data1.append(totaltime)
    data2.append(BloodLost)
    data3.append(TOTAL_LBS)
    # Save the data to a file
    with open(filename, "w") as file:
        for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{d1}\t{d2}\t{d3}\n")
#---------------------------------------            
    #Update Graph
    if TOTAL_LBS > running_max:
        running_max = TOTAL_LBS
    plt.plot(data1,data3,'b-', linewidth=2)
    plt.xlim(0, totaltime+15)
    plt.ylim(0, running_max + 10)
    plt.pause(0.1)
#---------------------------------------       
    #time refrence at the end of the cycle
    tic5 = time.perf_counter()
    totaltime = tic5-tic1
    print (totaltime)
#---------------------------------------     

    #Count the times through the loop
    L+=1
    print('Loopcount =', L)
#---------------------------------------   









#Direct Pressure
while method == 3 :
    #time stamp is taken
    tic2 = time.perf_counter()
    print('2')
    
#---------------------------------------
    #Collect Data, if error happens continue until there are 5 errors in a row then quit
    try :
        bus.write_byte(LOAD_SENSOR_ADDRESS2,dummy_command)#without this command, the status bytes go high on every other read
        bus.write_byte(LOAD_SENSOR_ADDRESS3,dummy_command)#without this command, the status bytes go high on every other read
        LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
        LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)
        print(3)
    except OSError:
        print('Error 1')
        sleep(.1)
        
        try :
            LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)
        except OSError:
            print('Error 2')
            sleep(.1)
            
            try :
                LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)  
            except OSError:
                print('Error 3')
                sleep(.1)
        
                try :
                    LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)  
                except OSError:
                    print('Error 4')
                    sleep(.1)
                    
                    try :
                        LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                        LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)
                    except OSError:
                        print('Error 5')
                        print('Stopping Motor and Turning off Solenoids')
                        GPIO.output(ENA, GPIO.HIGH)
                        GPIO.output(4, 0)
                        quit()  
 #---------------------------------------
        #Raw Data is turned into lbs and filtered
    LBS_DATA_SENSOR2=((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
    print ("Sensed load2 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000), "pounds")#plots out
    LBS_DATA_SENSOR3=((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
    print ("Sensed load3 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000), "pounds")#plots out
    
    
    
    if LBS_DATA_SENSOR3 < 0:
        LBS_DATA_SENSOR3 = 0
    if LBS_DATA_SENSOR3 > 0 and LBS_DATA_SENSOR3 <= upthreshold1:    
        STB_timer=0
    if LBS_DATA_SENSOR3 > upthreshold1 and LBS_DATA_SENSOR3 <= 40:
        LBS_DATA_SENSOR3 = upthreshold1
        STB_timer = STB_timer + cycletime
        if STB_timer >= 6:
            print('You Stopped The Bleed!!!')
            GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
            GPIO.output(4, 0)
            quit()
        
    if LBS_DATA_SENSOR3 > 40:
        LBS_DATA_SENSOR3 = 0 
    print('filtered data:',LBS_DATA_SENSOR3, 'Pounds')
#---------------------------------------
    Hz = -(LBS_DATA_SENSOR3) * ratio + output_max
    print(Hz)
#---------------------------------------
    #Motor is Enabled and frequency is set
    p.start(50) #PWM function is set to duty cycle of 50
    GPIO.output(ENA, GPIO.LOW)
    print('ENA set to LOW - Controller Enabled')
    GPIO.output(DIR, GPIO.HIGH)      #set Directin to CCW   
    p.ChangeFrequency(Hz)            #Update motor speed to new value of Hz
    p.ChangeDutyCycle(50)
#---------------------------------------      
    #time keeping, time start and measured against when motor settings are changed
    tic4 = tic3
    print('tic4=',tic4)
    tic3 = time.perf_counter()
    print('tic3=',tic3)
    if tic4 == 0:
        tic4 = tic3 - .3
        print('tic4=',tic4)
    cycletime = tic3 - tic4
    print ('cycletime =:',cycletime, 'seconds')
#---------------------------------------     

    #Count the times through the loop
    L+=1
    print('Loopcount =', L)
    
#---------------------------------------
    #Calculate Blood Loss
    Flow_Rate = 0.2643*math.log(Hz)-1.5221 #Liters per min
    BloodLost= BloodLost + (cycletime * Flow_Rate / 60)
    print('BloodLost is:', BloodLost, 'Liters')
  
    if BloodLost >= 3: #total blood lost to shut off machine, default is 3 (liters)
        GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
        GPIO.output(4, 0)          #turn off solenoid
        print('You were not fast enough, your patient lost over 3 liters of blood and died')
        quit()
#---------------------------------------
        #Add Progress bar with bloodlost data
#---------------------------------------   
    #Add data to lists
    data1.append(totaltime)
    data2.append(BloodLost)
    data3.append(LBS_DATA_SENSOR3)
    # Save the data to a file
    with open(filename, "w") as file:
        for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{d1}\t{d2}\t{d3}\n")
#---------------------------------------            
    #Update Graph
    if LBS_DATA_SENSOR3 > running_max:
        running_max = LBS_DATA_SENSOR3
    plt.plot(data1,data3,'b-', linewidth=2)
    plt.xlim(0, totaltime+15)
    plt.ylim(0, running_max + 10)
    plt.pause(0.1)
#---------------------------------------       
    #time refrence at the end of the cycle
    tic5 = time.perf_counter()
    totaltime = tic5-tic1
    print (totaltime)
#---------------------------------------     

    #Count the times through the loop
    L+=1
    print('Loopcount =', L)
#--------------------------------------- 










        
