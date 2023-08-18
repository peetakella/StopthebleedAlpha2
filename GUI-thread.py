from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from time import sleep
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import time #i2c ~~
import math
import smbus
import RPi.GPIO as GPIO #io~~
import matplotlib.pyplot as plt #graphing
import vlc
import threading
print ('Imoprts done')



#Initialise Variables------------------------------------------------------------------------------------------------------------------------------------------------------

# Fonts and texts
largetitletext = 105
mediumtitletext = 80
mediumtext = 30
smalltext = 25


L=0


#Initialise Variables-------------------------------------------------------------------------------------------------------------------------------------------------






root = Tk()
root.title("Better Bleeding Control")
print ('main thread', threading.get_ident())
root.configure(bg="grey75")
w = 1920
h = 1050
root.geometry("{}x{}".format(w, h))

#Add Title frame
frame1 = LabelFrame(root, pady=25, fg="black", bg="gray75")
frame1.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)

# Add a label at the top of the window
label_home = Label(frame1, text="Hemorrhage Control Trainer", font=("Arial", largetitletext), fg="black", bg="gray75")
label_home.pack(fill = X)
# Add two buttons underneath the label of home page

button_scenario = Button(root, text="Choose\nScenario", command = lambda: [open_scenario_window()], bg="firebrick3",fg="white",  font=("Arial", largetitletext), padx=10, pady=200)
button_scenario.place(x=.025*w, y=.25*h, height=.675*h, width=.47*w)
button_retrieve = Button(root, text="Retrieve\nData", command = lambda: [open_data_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
button_retrieve.place(x=.5025*w, y=.25*h, height=.675*h, width=.47*w)

def open_data_window():
#    root.after(1000, hide_root_window)
    data_window = Toplevel(root)
    data_window.title("Data")
    data_window.geometry("1024x600")
    data_window.configure(bg="grey75")
    data_window.attributes("-zoomed", True)  # Maximizes the window
    
    txtarea = Text(data_window, width=40, height=20)
    txtarea.grid(column = 0, row = 1)
    frame1 = LabelFrame(data_window, padx= 50, pady= 10, fg = 'black', bg = 'grey75')
    frame1.grid(row= 1, column= 1, columnspan= 1, padx= 25, pady= 20)

    label_file_explorer = Label(data_window, text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")
    label_file_explorer.grid(column = 0, row = 0, columnspan= 2)
      
    button_explore = Button(data_window, text = "Browse Files", command = browseFiles)
    button_explore.grid(column = 0, row = 4)  

    button_exit = Button(data_window, text = "Exit", command = exit)
    button_exit.grid(column = 0,row = 5)

    fig = Figure()
    ax = fig.add_subplot(111)
    line, = ax.plot(x, m)
    #line_20ref, = ax.plot(x. ma_x)

    canvas = FigureCanvasTkAgg(fig, master= frame1)
    canvas.draw()
    canvas.get_tk_widget().grid(column = 1, row = 1)

def open_scenario_window():
    global wound, sound, blood
    # Create the scenario window
    scenario_window = Toplevel(root)
    scenario_window.title("Choose Scenario")
    scenario_window.geometry("{}x{}".format(w, h))
    scenario_window.configure(bg="gray75")

    #Add Title frame
    framet = LabelFrame(scenario_window,fg="black", bg="gray75")
    framet.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)    
    # Add a label at the top of the window
    label_scenario = Label(framet, text="Choose Scenario", font=("Arial", largetitletext), fg="black", bg="gray75", pady = 15)
    label_scenario.pack(fill = X)
    
    #Add the Frames
    #Add left frame
    frameL = LabelFrame(scenario_window,bg="firebrick3", fg="white")
    frameL.place(x=.015*w, y=.25*h, height=.675*h, width=.3*w)     
    #Add Middle frame
    frameM = LabelFrame(scenario_window, padx=50, pady=5,bg="firebrick3", fg="white")
    frameM.place(x=.345*w, y=.25*h, height=.325*h, width=.3*w)            
    #Add Right Frame
    frameR = LabelFrame(scenario_window, padx=50, pady=5,bg="firebrick3", fg="white")
    frameR.place(x=.675*w, y=.25*h, height=.675*h, width=.3*w)

    # Add the left section with wound choice checkboxes
    label_wound_choice = Label(frameL, text="Wound:", bg="firebrick3", fg="white",font=("Arial", largetitletext), padx= 40)
    label_wound_choice.grid(row=0, column=0, pady=0)    
    # Add the checkboxes for wound choice
    wound = 1  #1=upper and 2=lower  
    checkbox_junction = Radiobutton(frameL, text="Upper",font=("Arial", mediumtitletext), variable = wound, value=1,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=90, indicatoron=0,bd=10)
    checkbox_junction.grid(row=1, column=0,padx=0, pady=10)
    checkbox_arm = Radiobutton(frameL, text="Lower",font=("Arial", mediumtitletext), variable = wound, value=2,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=90, indicatoron=0,bd=10)
    checkbox_arm.grid(row=2, column=0,padx=0,pady=10)
    # Add the middle section with sound toggle switch
    label_sound = Label(frameM, text="Sound:", font=("Arial", largetitletext),bg="firebrick3", fg="white")
    label_sound.grid(row=0, column=0,columnspan=2, pady=0)    
    # Add the sound toggle switch
    sound = 2
    checkbox_on = Radiobutton(frameM, text="On",font=("Arial", mediumtitletext), variable=sound, value=1,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=10, indicatoron=0,bd=10)
    checkbox_on.grid(row=1, column=0,padx=0, pady=0)
    checkbox_off = Radiobutton(frameM, text="Off",font=("Arial", mediumtitletext), variable=sound, value=2,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=5, indicatoron=0,bd=10)
    checkbox_off.grid(row=1, column=1,padx=0,  pady=0)
    
    #Button to enter scenario in middle frame
    button_scenario = Button(scenario_window, text="Begin", command = lambda: [call_both_functions()],  font=("Arial", largetitletext),bg="firebrick3",fg="white")
    button_scenario.place(x=.345*w, y=.6*h, height=.15*h, width=.3*w)
    button_quit = Button(scenario_window, text="Home", command = lambda: [scenario_window.destroy()],  font=("Arial", largetitletext),bg="firebrick3",fg="white")
    button_quit.place(x=.345*w, y=.775*h, height=.15*h, width=.3*w)

    # Add the right section with bleed out time checkboxes
    label_bleed = Label(frameR, text="Blood:", font=("Arial", largetitletext),bg="firebrick3", fg="white")
    label_bleed.grid(row=0, column=0, pady=0)
    # Add the checkboxes for bleed out time
    blood = 3
    checkbox_high = Radiobutton(frameR, text="High",font=("Arial", mediumtitletext), variable=blood, value=1,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=110, indicatoron=0,bd=10)
    checkbox_high.grid(row=1, column=0,padx=0, pady=10)
    checkbox_low = Radiobutton(frameR, text="Low",font=("Arial", mediumtitletext), variable=blood, value=2,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=125, indicatoron=0,bd=10)
    checkbox_low.grid(row=2, column=0,padx=0,  pady=10)
    checkbox_off = Radiobutton(frameR, text="Off",font=("Arial", mediumtitletext), variable=blood, value=3,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=150, indicatoron=0,bd=10)
    checkbox_off.grid(row=3, column=0,padx=0,  pady=10)
    

#    scenario_window.destroy()
def call_both_functions():
    thd1 = threading.Thread(target=Background)
    thd1.daemon = True
    thd1.start()    
    open_sim_window()
    
def open_sim_window():
    print ('wound', wound)
    print ('Sound', sound)
    print ('blood', blood)       
    
    sim_window = Toplevel(root)
    sim_window.title("Simulation")
    #sim_window.geometry("1024x600")
    sim_window.configure(bg="grey75")
    sim_window.attributes("-zoomed", True)  # Maximizes the window
    #sim_window.attributes("-fullscreen", True)  # substitute `Tk` for whatever your `Tk()` object is called  

           
    bleedoutbarframe = LabelFrame(sim_window,bg="firebrick3", fg="white")
    bleedoutbarframe.grid(row=0, column=0)
    graphframe = LabelFrame(sim_window,bg="firebrick3", fg="white")
    graphframe.grid(row=0, column=1)
    
    # Add the frame that the bleedout bar will go in
    label_bleedoutbar = Label(bleedoutbarframe, text="Blood\nLost", bg="firebrick3", fg="white", font=("Arial", mediumtitletext), padx=70, pady=10)
    label_bleedoutbar.grid(row=0, column=0,columnspan=2, sticky="w")
    axis_bleedoutbar = Label(bleedoutbarframe, text='-    3.0\n\n-    2.5\n\n-    2.0\n\n-    1.5\n\n-    1.0\n\n-    0.5\n\n- 0.0 (L)', font=('Arial', 35), fg="white", bg="firebrick3")
    axis_bleedoutbar.grid(row=1, column = 1)
    progbar = ttk.Progressbar(bleedoutbarframe,length=750, orient="vertical", mode="determinate",takefocus=True, maximum=10)       
    progbar.grid(row=1, column=0, ipadx=130)
    progbar.start
    progbar['value'] = 0
    print(3333333333333333333)    
    # Add the frame hat the graph will go in
    plt.rcParams.update({'font.size':22})
    fig = Figure(figsize=(15, 10.1))        
    x = [0,1,2,3,4,5,6,7,8,9]
    m = [0,2,4,6,8,6,2,3,8,5]
    ma_x = [20,20,20,20,20,20,20,20,20,20]
        
    ax = fig.add_subplot(111)
    ax.set_title('Pressure', fontsize=80)
    ax.set_xlabel('Time (s)', fontsize=40)
    ax.set_ylabel('Pressure at Bleed (LBS)', fontsize=40)
    line, = ax.plot(x, m, label='Your Pressure', linewidth=5)
    line_20ref, = ax.plot(x, ma_x, label='Target Pressure', linewidth=5)
    ax.legend(loc='upper left', fontsize=20)
    
    # Add the canvas for the graph
    canvas_graph = FigureCanvasTkAgg(fig, master=graphframe)  # A tk.DrawingArea.
    canvas_graph.draw()
    canvas_graph.get_tk_widget().grid(row=1,column=0)
    
    
    
    def Update_Sim_Window(event1):
        print(event1.state)    
        big_BloodLost1 = float(event1.state)
        BloodLost1 = big_BloodLost1 / 100000000    
        print('BloodLost1:',BloodLost1)
        BloodLost1=BloodLost1*200
        progbar['value'] = BloodLost1
        
    sim_window.bind("<<event1>>",Update_Sim_Window)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#^^^^^GUI^^^         \/ \/ \/ Backend \/ \/ \/
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
















#------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#Sounds------------------------------------------------------------------------------------------------------------------------------------------------ 

scream1 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v1.mp3")
scream2 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v2.mp3")
scream3 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v3.mp3")
scream4 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v4.mp3")
scream5 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Scream_v5.mp3")
help_me1 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Help Me Loud_v1.mp3")
help_me2 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Help Me Loud_v2.mp3")
gasp1 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Gasp_v1.mp3")
gasp2 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Gasp_v2.mp3")
gasp3 = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/Gasp_v3.mp3")
Background_Sound = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/police-siren-water-cannon-tear-gas-people-coughing-and-protesters-throwing-stones-at-the-police-during-the-chilean-uprising-november-2019-24871.mp3")
you_failed = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/you_failed.mp3")
you_succeded = vlc.MediaPlayer("/home/stopthebleed/StoptheBleed/Sounds/you_succeded1.mp3")

#Sounds-------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
def Background():
    while 1:
        sleep(.25)
        print('loop begin')
        global blood, wound, sound, L
        if L == 0:
            MAX_MOTOR_SPEED = 12000  # Initialize with a default value
            #name file to save data to
            '''name = input ("enter trial run name")
            filename=(f"{name}.txt")'''
            filename = (f"A - Previous Trial.txt")
            #TODO Throw error codes for when and if there is something that can't be in a file name and have them try again
            open(filename,"w")
            print (filename)
            tic3 = 0 #timestamp
            cycletime = 0
            print('1')
            tic1 = time.perf_counter()
            print('blood:',blood)
            if blood == 1:     #2:30 also known as high
                MAX_MOTOR_SPEED = 14000
            if blood == 2:     #5:00 also known as low
                MAX_MOTOR_SPEED = 2500
            print(MAX_MOTOR_SPEED)
            #if blood is 3, liquid is off

            timetostopthebleed = 6
            running_max = 0
            upthreshold1 = 20
            upthreshold2 = 20
            upthreshold3 = 20
            errorthreshold1 = 40
            errorthreshold2 = 40
            errorthreshold3 = 40


            #Motor speed value is set
            input_min = 0
            input_max1 = upthreshold1
            input_max2 = upthreshold2
            input_max3 = upthreshold3
            output_min = 100 #frequency in hz, higher is faster pumping
            output_max = MAX_MOTOR_SPEED

            # Calculate the ratio
            ratio1 = (output_max - output_min) / (input_max1 - input_min)
            ratio2 = (output_max - output_min) / (input_max2 - input_min)
            ratio3 = (output_max - output_min) / (input_max3 - input_min)
            
            x1=0
            x2=0
            x3=0
            x4=0
            x5=0
            x6=0
            x7=0
            x8=0
            totaltime = 0
            BloodLost = 0
            bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
            
            channel = 1          #select channel
            #set up digital io
            GPIO.setwarnings(False)           #do not show any warnings
            GPIO.setmode (GPIO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
            GPIO.setup(19,GPIO.OUT)       # initialize GPIO19 as an output, not important for the pressure sensor or load cell

            PUL = 12  #pwm pin
            DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
            ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(PUL, GPIO.OUT)
            GPIO.setup(DIR, GPIO.OUT)
            GPIO.setup(ENA, GPIO.OUT)
            arm = 18
            junction = 4    
            GPIO.setup(arm, GPIO.OUT)
            GPIO.setup(junction, GPIO.OUT)
            p=GPIO.PWM(PUL, 100) #PWM Function is defined
            
            #Condition sensor for continuous measurements
            LOAD_SENSOR_ADDRESS1=0x28 #junction
            LOAD_SENSOR_ADDRESS2=0x27 #Higher arm sensor
            LOAD_SENSOR_ADDRESS3=0x26 #Lower arm sensor
            dummy_command=0x00
            offset=1000    
            #offset=int((input("Enter offset value, default 1000:") or 1000))                                        #subtracts zero offset per data sheet, should be 1000
            LOAD_SENSOR_DATA1=bus.read_byte(LOAD_SENSOR_ADDRESS1)#This apparently turns the load sensor on, only need it once
            LOAD_SENSOR_DATA2=bus.read_byte(LOAD_SENSOR_ADDRESS2)
            LOAD_SENSOR_DATA3=bus.read_byte(LOAD_SENSOR_ADDRESS3)
            LBS_DATA_SENSOR1=0
            LBS_DATA_SENSOR2=0
            LBS_DATA_SENSOR3=0

            #Create empty lists
            data1 = []
            data2 = []
            data3 = []
            data4 = []

    #Set one time things-----------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #Collect Data, if error happens continue until there are 5 errors in a row then quit---------------------------------------------------------------------------------------------------
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
                            stop_pump()
                            sleep(5)
                            quit()
        try :
            bus.write_byte(LOAD_SENSOR_ADDRESS1,dummy_command)#without this command, the status bytes go high on every other read
            LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            print(3)
        except OSError:
            print('Error 1')
            sleep(.1)
            
            try :
                LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            except OSError:
                print('Error 2')
                sleep(.1)
                
                try :
                    LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    print('Error 3')
                    sleep(.1)
            
                    try :
                        LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        print('Error 4')
                        sleep(.1)
                        
                        try :
                            LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                        except OSError:
                            print('Error 5')
                            print('Stopping Motor and Turning off Solenoids')
                            stop_pump()
                            sleep(5)
                            quit()
        try :
            bus.write_byte(LOAD_SENSOR_ADDRESS3,dummy_command)#without this command, the status bytes go high on every other read
            LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            print(3)
        except OSError:
            print('Error 1')
            sleep(.1)
            
            try :
                LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
            except OSError:
                print('Error 2')
                sleep(.1)
                
                try :
                    LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    print('Error 3')
                    sleep(.1)
            
                    try :
                        LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        print('Error 4')
                        sleep(.1)
                        
                        try :
                            LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                        except OSError:
                            print('Error 5')
                            print('Stopping Motor and Turning off Solenoids')
                            stop_pump()
                            sleep(5)
                            quit()                              
#Collect Data------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------
#Raw Data is turned into lbs and filtered----------------------------------------------------------------------------------------------------
        print('Raw sensor data 1:',LBS_DATA_SENSOR1)
        print('Raw sensor data 1:',LBS_DATA_SENSOR1)
        print('Raw sensor data 1:',LBS_DATA_SENSOR1)
        
        LBS_DATA_SENSOR1=((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
        print ("Sensed load in LBS 1 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000), "pounds")#plots out       
        LBS_DATA_SENSOR1 = 1.5 * LBS_DATA_SENSOR1
        if LBS_DATA_SENSOR1 < 0:
            LBS_DATA_SENSOR1 = 0
        if LBS_DATA_SENSOR1 > 0 and LBS_DATA_SENSOR1 <= upthreshold1:  #upthreshpld line 300  
            STB_timer=0
        if LBS_DATA_SENSOR1 > upthreshold1 and LBS_DATA_SENSOR1 <= errorthreshold1:
            LBS_DATA_SENSOR1 = upthreshold1
        if LBS_DATA_SENSOR1 > errorthreshold1:
            LBS_DATA_SENSOR1 = 0
        

                

        LBS_DATA_SENSOR2=((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
        print ("Sensed load in LBS 2 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000), "pounds")#plots out       
        LBS_DATA_SENSOR2 = 1.5 * LBS_DATA_SENSOR2
        if LBS_DATA_SENSOR2 < 0:
            LBS_DATA_SENSOR2 = 0
        if LBS_DATA_SENSOR2 > 0 and LBS_DATA_SENSOR2 <= upthreshold2:  #upthreshpld line 300  
            STB_timer=0
        if LBS_DATA_SENSOR2 > upthreshold2 and LBS_DATA_SENSOR2 <= errorthreshold2:
            LBS_DATA_SENSOR2 = upthreshold2
        if LBS_DATA_SENSOR1 > errorthreshold2:
            LBS_DATA_SENSOR1 = 0 


        LBS_DATA_SENSOR3=((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
        print ("Sensed load in LBS 3 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000), "pounds")#plots out       
        LBS_DATA_SENSOR3 = 1.5 * LBS_DATA_SENSOR3
        if LBS_DATA_SENSOR3 < 0:
            LBS_DATA_SENSOR3 = 0
        if LBS_DATA_SENSOR3 > 0 and LBS_DATA_SENSOR3 <= upthreshold3:  #upthreshpld line 300  
            STB_timer=0 
        if LBS_DATA_SENSOR3 > upthreshold3 and LBS_DATA_SENSOR3 <= errorthreshold3:
            LBS_DATA_SENSOR3 = upthreshold3
        if LBS_DATA_SENSOR1 > errorthreshold3:
            LBS_DATA_SENSOR1 = 0
        
        if wound == 1:
            if LBS_DATA_SENSOR1 > upthreshold1 and LBS_DATA_SENSOR1 <= errorthreshold1:
                STB_timer += cycletime        
        if wound == 2:    
            if LBS_DATA_SENSOR2+LBS_DATA_SENSOR3 > upthreshold3 and LBS_DATA_SENSOR2+LBS_DATA_SENSOR3 <= errorthreshold3:
                STB_timer += cycletime            
            
            
        print('filtered data:', LBS_DATA_SENSOR1, 'Pounds')
        print('filtered data:', LBS_DATA_SENSOR2, 'Pounds')
        print('filtered data:', LBS_DATA_SENSOR3, 'Pounds')
        
#Raw Data is turned into lbs and filtered------------------------------------------------------------------------------------------------------------       
#----------------------------------------------------------------------------------------------------------------------------------------------------
#set motor Hz----------------------------------------------------------------------------------------------------------------------------------------            
        
        Hz1 = -(LBS_DATA_SENSOR1) * ratio1 + output_max
        print('Hz1:',Hz1)
        Hz2 = -(LBS_DATA_SENSOR2+LBS_DATA_SENSOR2) * ratio2 + output_max #both arm pressure sensors data is added together to make the tourniquet/direct pressure setting
        print('Hz2:',Hz2)
        Hz3 = -(LBS_DATA_SENSOR3) * ratio3 + output_max
        print('Hz3:',Hz3)

#Set motor Hz------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------
#Turn Motor on and update pwm----------------------------------------------------------------------------------------------------------------------------

        
        
        if wound == 1 and blood <= 2:
            #This Turns Relay On. 
            GPIO.output(junction, 1)
            #Motor is Enabled and frequency is set
            p.start(50) #PWM function is set to duty cycle of 50
            GPIO.output(DIR, GPIO.HIGH)      #set Directin to CCW 
            GPIO.output(ENA, GPIO.LOW)  #enable motor
            print('ENA set to LOW - Controller Enabled')
              
            p.ChangeFrequency(Hz1)            #Update motor speed to new value of Hz
            p.ChangeDutyCycle(50)
        
        if wound == 2 and blood <= 2:
            #This Turns Relay On. 
            GPIO.output(arm, 1)
            #Motor is Enabled and frequency is set
            p.start(50) #PWM function is set to duty cycle of 50
            GPIO.output(DIR, GPIO.HIGH)      #set Directin to CCW 
            GPIO.output(ENA, GPIO.LOW)  #enable motor
            print('ENA set to LOW - Controller Enabled') 
            p.ChangeFrequency(Hz2)            #Update motor speed to new value of Hz
            p.ChangeDutyCycle(50)            

#Turn Motor on and update pwm----------------------------------------------------------------------------------------------------------------------------   
#-------------------------------------------------------------------------------------------------------------------------------------------------------      
#time keeping, cycle time total time and loop count-------------------------------------------------------------------------------------------------------
            
        tic4 = tic3
        print('tic4=',tic4)
        tic3 = time.perf_counter()
        print('tic3=',tic3)
        if tic4 == 0:
            tic4 = tic3 - .3
            print('tic4=',tic4)
        cycletime = tic3 - tic4
        print ('cycletime =:',cycletime, 'seconds')
        
        tic5 = time.perf_counter()
        totaltime = tic5-tic1
        print (totaltime)        
        #Count the times through the loop
        L+=1
        print('Loopcount =', L)
        
#time keeping, cycle time total time and loop count---------------------------------------------------------------------------        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Calculate Blood Loss-------------------------------------------------------------------------------------------------------------------------------------------------------
        if  wound == 1:  
            Flow_Rate = 0.2643*math.log(Hz1)-1.5221 #Liters per min
            BloodLost= BloodLost + (cycletime * Flow_Rate / 60)
            print('BloodLost is:', BloodLost, 'Liters')
        if  wound == 2:  
            Flow_Rate = 0.2643*math.log(Hz2)-1.5221 #Liters per min
            BloodLost= BloodLost + (cycletime * Flow_Rate / 60)
            print('BloodLost is:', BloodLost, 'Liters')          
        
        if BloodLost >= 3: #total blood lost to shut off machine, default is 3 (liters)
            stop_pump()
            print('You were not fast enough, your patient lost over 3 liters of blood and died')
            sleep(5)
            #quit() #TODO end thread and go back to home

        
        rounded_BloodLost = round(BloodLost, 8)  # Rounds to 8 decimal places
        big_bloodLost = rounded_BloodLost*100000000
        int_BloodLost = int(big_bloodLost)
        print('big_bloodlost:',int_BloodLost)  # Outputs: 3.14159265

#Calculate Blood Loss-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#sound playing----------------------------------------------------------------------------------------------------------------------------------------------------------
        if sound == 1:
            b=BloodLost
            if wound == 1:
                p = LBS_DATA_SENSOR1
            if wound == 2:
                p = LBS_DATA_SENSOR2+LBS_DATA_SENSOR2
            if b >= .25 and x1 == 0:
                help_me2.play()
                x1=1
            if b >= .5 and x2 == 0:
                x2=1
            if b >= 1.5 and x3 == 0:
                x3=1    
            if b >= 2.5 and x4 == 0:
                x4=1
            if p >= 20 and x5 == 0:
                T.insert(END,"\n" + "Hold at least this much pressure for at least 6 secconds")
                x5=1
                scream4.play()
                sleep (.75)
                scream4.stop()
                scream3.play()
                sleep (.65)
                scream3.stop()
                scream2.play()
                sleep (.75)
                scream2.stop()
                scream1.play()
                sleep (.65)
                scream1.stop()
                scream4.play()
                sleep (.75)
                scream4.stop()
                scream5.play()
                sleep (.65)
                scream5.stop()
                scream1.play()
                sleep (.75)
                scream1.stop()
                scream3.play()
                sleep (.65)
                scream3.stop()
                x5=0
            if p >= 10 and x6 == 0 and method == 1:
                x6=1
            if p >= 15 and x7 == 0 and method == 1:
                scream4.play()            
                x7=1    
            if p >= 2.5 and x8 == 0:
                gasp1.play()
                x8=1



#sound playing----------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#STB timer reaches end------------------------------------------------------------------------------------------------------------------------------------------------------
                
        if STB_timer >= timetostopthebleed:
            stop_pump()
            print('You Stopped the bleed')
            sleep(5)
            if sound == 1:
                you_succeded.play()
                
                    
                    
#STB timer reaches end------------------------------------------------------------------------------------------------------------------------------------------------------                    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Add data to lists and save file--------------------------------------------------------------------------------------------------------------------------------------------

        data1.append(totaltime)
        data2.append(BloodLost)
        if wound == 1:
            data3.append(LBS_DATA_SENSOR1)
            DATA = LBS_DATA_SENSOR1
        if wound == 2:
            data3.append(LBS_DATA_SENSOR2+LBS_DATA_SENSOR3)
            DATA=LBS_DATA_SENSOR2+LBS_DATA_SENSOR3
        # Save the data to a file
        with open(filename, "a") as file:
            #for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{totaltime}\t{BloodLost}\t{DATA}\n")
            
#Add Data t list and save file-------------------------------------------------------------------------------------------------------------------------------            
#-------------------------------------------------------------------------------------------------------------------------------------------------------------            
#create events for GUI, pass Data------------------------------------------------------------------------------------------------------------------------------------
            
        sleep(.25)     
        root.event_generate("<<event1>>", state=str(int_BloodLost))     
        sleep(.25)    
        print('event generated')    
            
            

#create events for GUI, pass Data------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------       
#time refrence at the end of the cycle and loop count----------------------------------------------------------------------------------------------------------
        

        
#time refrence at the end of the cycle and loop count----------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------   
#stop pump and solenoid function-------------------------------------------------------------------------------------------------------------------------------     
        def stop_pump():
            GPIO.output(ENA, GPIO.HIGH)
            GPIO.output(junction, 0)
            GPIO.output(arm,0)
            

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 


 




mainloop()