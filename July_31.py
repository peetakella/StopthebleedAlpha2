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
from time import sleep
import RPi.GPIO as GPIO #io~~
import matplotlib.pyplot as plt #graphing
import vlc
import threading
print ('Imoprts done')
#sounds VLC
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
# Create the main window
root = Tk()
root.title("Better Bleeding Control")
root.configure(bg="grey75")
root.attributes("-zoomed", True)  # Maximizes the window
#root.attributes("-fullscreen", True)  # substitute `Tk` for whatever your `Tk()` object is called

global largetitletext, mediumtitletext, mediumtext, smalltext
largetitletext = 80
mediumtitletext = 60
mediumtext = 30
smalltext = 25

#Add Title frame
frame1 = LabelFrame(root, padx=50, pady=10,fg="black", bg="gray75")
frame1.grid(row=0, column=0,columnspan=2,pady=20, padx=25)

# Add a label at the top of the window
label_home = Label(frame1, text="Hemorrhage Control Trainer", font=("Arial", largetitletext), fg="black", bg="gray75")
label_home.grid(row=0, column=0,  pady=20, padx=10)
# Add two buttons underneath the label of home page

button_scenario = Button(root, text="Choose \n Scenario", command = lambda: [open_scenario_window()], bg="firebrick3",fg="white",  font=("Arial", largetitletext), padx=50, pady=300)
button_scenario.grid(row=1, column=0, padx=100, pady=20)
button_retrieve = Button(root, text="Retrieve \n Data", command = lambda: [open_data_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=100, pady=300)
button_retrieve.grid(row=1, column=1, padx=100, pady=20)

#def hide_root_window():
#    root.withdraw()
#def hide_scenario_window():
#    scenario_window.withdraw()
#def hide_root_window():
#    root.withdraw()
    
def open_data_window4():
#    root.after(1000, hide_root_window)
    print ('enter open_data_window function')
    data_window = Toplevel(root)
    data_window.title("Data")
    data_window.geometry("1024x600")
    data_window.configure(bg="grey75")
    data_window.attributes("-zoomed", True)  # Maximizes the window
    global filename

    def browseFiles():
        print ('enter browseFiles function')
        filename = filedialog.askopenfilename(initialdir = "/home/stopthebleed/Stopthebleed", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
        
        '''label_file_explorer = Label(datatitleframe1, text = "Find Past Training Excersises", font=("Arial", mediumtext), fg="black", bg="gray75")
        label_file_explorer.grid(row=0, column=0, columnspan=2, pady=20, padx=10)'''
        label_file_explorer.configure(text="File Opened: "+filename, font=("Ariel", mediumtext), fg="black", bg="gray75")

        with open(filename, 'r') as f:
            #configfile.insert(INSERT, f.read())
            data = f.read()

        pathh.insert(END, filename)
        text_area.insert(END, data)
        #filename.close()

        return filename
        print (filename)

    #configfile = Text(data_window, wrap=WORD, width=45, height= 20)

    text_area = Text(data_window, width=100, height=40)
    text_area.grid(column = 1, row = 1)

    #pathh.grid(column = 1, row = 2)
    #Add Title frame
    datatitleframe1 = LabelFrame(data_window, padx=20, pady=10,fg="black", bg="gray75")
    datatitleframe1.grid(row=0, column=0,columnspan=2,pady=20, padx=25)
    
    label_file_explorer = Label(datatitleframe1, text = "Find Past Training Excersises", font=("Arial", largetitletext), fg="black", bg="gray75")
    label_file_explorer.grid(row=0, column=0, columnspan=2, pady=20, padx=10)
    

    button_explore = Button(data_window, text = "Browse Files", command = browseFiles, bg="firebrick3",fg="white",  font=("Arial", mediumtitletext), padx=50, pady=300 )
    button_explore.grid(column = 0, row = 1)  

    button_exit = Button(data_window, text = "Exit", command = exit)
    button_exit.grid(column = 0,row = 2)




    #with open(filename, 'r') as f:
        #configfile.insert(INSERT, f.read())'''
        
def open_data_window():
#    root.after(1000, hide_root_window)
    data_window = Toplevel(root)
    data_window.title("Data")
    data_window.geometry("1024x600")
    data_window.configure(bg="grey75")
    data_window.attributes("-zoomed", True)  # Maximizes the window
    
    global filename, x, m, ma_x

    x = []
    m = []
    ma_x = []


    def browseFiles():
        #global x, m, ma_x
        
        filename = filedialog.askopenfilename(initialdir = "/home/stopthebleed/StoptheBleed", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))

        label_file_explorer.configure(text="File Opened: "+filename)
        
        for line in open(filename, 'r'):
            data = [i for i in line.split()]
            x.append(float(data[0]))
            m.append(float(data[2]))
            
        
        with open(filename, 'r') as f:
            #configfile.insert(INSERT, f.read())
            data = f.read()
           
            
        pathh.insert(END, filename)
        txtarea.insert(END, data)
        
        #print(x[0:12])
        #print(m[0:12])
        
        #filename.close()
        update_graph()

        
        return filename

    #configfile = Text(data_window, wrap=WORD, width=45, height= 20)

    txtarea = Text(data_window, width=40, height=20)
    txtarea.grid(column = 0, row = 1)
    #txtarea.pack(pady=20)

    frame1 = LabelFrame(data_window, padx= 50, pady= 10, fg = 'black', bg = 'grey75')
    frame1.grid(row= 1, column= 1, columnspan= 1, padx= 25, pady= 20)

    pathh = Entry(data_window)
    pathh.grid(column = 0, row = 3)
    #pathh.pack(side=LEFT, expand=True, fill=X, padx=20)

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

    def update_graph():
        
        line.set_data(x, m)
        #line_20ref.setdata(x, ma_x)
        ax.relim()
        ax.autoscale_view()
        canvas.draw()
        #print(x[0:12])
        #print(m[0:12])


def open_scenario_window():
#    root.after(1000, hide_root_window)
    global method, sound, liquid, speed
    
    # Create the scenario window
    scenario_window = Toplevel(root)
    scenario_window.title("Choose Scenario")
    #scenario_window.geometry("1024x600")
    scenario_window.configure(bg="gray75")
    scenario_window.attributes("-zoomed", True)  # Maximizes the window
    #Add Title frame
    framet = LabelFrame(scenario_window, padx=50, pady=10,fg="black", bg="gray75")
    framet.grid(row=0, column=0,columnspan=3,pady=20, padx=25)    
    # Add a label at the top of the window
    label_scenario = Label(framet, text="Choose Scenario", font=("Arial", largetitletext), fg="black", bg="gray75")
    label_scenario.grid(row=0, column=0, pady=35)
    
    #Add the Frames
    #Add left frame
    frameL = LabelFrame(scenario_window, padx=50, pady=5,bg="firebrick3", fg="white")
    frameL.grid(row=1, column=0,padx=50,pady=25)     
    #Add Middle frame
    frameM = LabelFrame(scenario_window, padx=50, pady=5,bg="firebrick3", fg="white")
    frameM.grid(row=1, column=1,padx=0,pady=25)            
    #Add Right Frame
    frameR = LabelFrame(scenario_window, padx=50, pady=5,bg="firebrick3", fg="white")
    frameR.grid(row=1, column=2,padx=50,pady=25)


    # Add the left section with wound choice checkboxes
    label_wound_choice = Label(frameL, text="Practice Method", bg="firebrick3", fg="white",font=("Arial", mediumtitletext))
    label_wound_choice.grid(row=0, column=0, pady=60)    
    # Add the checkboxes for wound choice
    method = IntVar()    
    checkbox_junction = Checkbutton(frameL, text="Wound Packing",font=("Arial", smalltext), variable = method, onvalue = 1, bg="firebrick3", fg="white", selectcolor="black",padx=5)
    checkbox_junction.grid(row=1, column=0,padx=5, pady=15)
    checkbox_arm = Checkbutton(frameL, text="Tourniquet",font=("Arial", smalltext), variable = method, onvalue = 2, bg="firebrick3", fg="white", selectcolor="black",padx=5)
    checkbox_arm.grid(row=2, column=0,padx=5,pady=15)
    checkbox_hand = Checkbutton(frameL, text="Direct Pressure",font=("Arial", smalltext), variable = method, onvalue = 3, bg="firebrick3", fg="white", selectcolor="black",padx=5)
    checkbox_hand.grid(row=3, column=0,padx=5,pady=15)
    # Add the middle section with sound toggle switch
    label_sound = Label(frameM, text="Sound", font=("Arial", mediumtitletext),bg="firebrick3", fg="white")
    label_sound.grid(row=0, column=0, pady=60)    
    # Add the sound toggle switch
    sound = IntVar()
    toggle_switch = Checkbutton(frameM, text="On/Off",font=("Arial", smalltext), variable=sound, onvalue=1, offvalue=0,bg="firebrick3", fg="white", selectcolor="black",padx=5)
    toggle_switch.grid(row=1, column=0, pady=0)
     # Add the middle section with liquid toggle switch
    label_liquid = Label(frameM, text="liquid", font=("Arial", mediumtitletext),bg="firebrick3", fg="white")
    label_liquid.grid(row=2, column=0, pady=40)    
    # Add the liquid toggle switch
    liquid = IntVar()
    toggle_switch = Checkbutton(frameM, text="On/Off",font=("Arial", smalltext), variable=liquid, onvalue=1, offvalue=0,bg="firebrick3", fg="white", selectcolor="black",padx=5)
    toggle_switch.grid(row=3, column=0,pady=15)

    # Add the right section with bleed out time checkboxes
    label_bleed_out = Label(frameR, text="Bleed out time", font=("Arial", mediumtitletext),bg="firebrick3", fg="white")
    label_bleed_out.grid(row=0, column=0, columnspan=2, pady=60)
    # Add the checkboxes for bleed out time
    speed = IntVar()
    checkbox_2_30 = Radiobutton(frameR, text="2:30",font=("Arial", smalltext), variable=speed, value=1,bg="firebrick3", fg="white", selectcolor="black",padx=5)
    checkbox_2_30.grid(row=1, column=0,padx=10, pady=15)
    checkbox_3_00 = Radiobutton(frameR, text="3:00",font=("Arial", smalltext), variable=speed, value=2,bg="firebrick3", fg="white", selectcolor="black",padx=5)
    checkbox_3_00.grid(row=1, column=1,padx=10,  pady=15)
    checkbox_3_30 = Radiobutton(frameR, text="3:30",font=("Arial", smalltext), variable=speed, value=3,bg="firebrick3", fg="white", selectcolor="black",padx=5)
    checkbox_3_30.grid(row=2, column=0,padx=10,  pady=15)
    checkbox_4_00 = Radiobutton(frameR, text="4:00",font=("Arial", smalltext), variable=speed, value=4,bg="firebrick3", fg="white", selectcolor="black",padx=5)
    checkbox_4_00.grid(row=2, column=1,padx=10,  pady=15)
    checkbox_4_30 = Radiobutton(frameR, text="4:30",font=("Arial", smalltext), variable=speed, value=5,bg="firebrick3", fg="white", selectcolor="black",padx=5)
    checkbox_4_30.grid(row=3, column=0,padx=10,  pady=15)
    checkbox_5_00 = Radiobutton(frameR, text="5:00",font=("Arial", smalltext), variable=speed, value=6,bg="firebrick3", fg="white", selectcolor="black",padx=5)
    checkbox_5_00.grid(row=3, column=1,padx=10,  pady=15)
    
    print ('method', method.get())
    print ('Sound', sound.get())
    print ('liquid', liquid.get())
    print ('Speed', speed.get())
    
    #Button to enter scenario
    button_scenario = Button(scenario_window, text="Begin", command = lambda: [function(method.get(), speed.get(), liquid.get())],  font=("Arial", mediumtitletext),bg="firebrick3",fg="white", padx=30)
    button_scenario.grid(row=2, column=1, padx=50, pady=5)
#----------------------------------------------------------------------------------

x1=0
x2=0
x3=0
x4=0
x5=0
x6=0
x7=0
x8=0
def function(m, s, l):
    
    #set up i2c
    tic0 = time.perf_counter()
    bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
    sleep(1)
    channel = 1          #select channel
    #Background_Sound.play()
    #set up digital io
    GPIO.setwarnings(False)           #do not show any warnings
    GPIO.setmode (GPIO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    GPIO.setup(19,GPIO.OUT)       # initialize GPIO19 as an output, not important for the pressure sensor or load cell

    #set up graph

    running_max = 0
    upthreshold1 = 20
    upthreshold2 = 20
    upthreshold3 = 20


    #Variables from GUI
    method = m #1 for junction, 2 for tourniquet, 3 for Direct Pressure
    BLEEDOUT_TIME = s #1-6 number being passed through global variable (speed in gui)

 
    PUL = 12  #pwm pin
    DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
    ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
    
    GPIO.setmode(GPIO.BCM)
    # GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only. 
    #
    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    arm = 18
    junction = 4    
    GPIO.setup(arm, GPIO.OUT)
    GPIO.setup(junction, GPIO.OUT)
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
    LOAD_SENSOR_DATA2=bus.read_byte(LOAD_SENSOR_ADDRESS2)
    LOAD_SENSOR_DATA3=bus.read_byte(LOAD_SENSOR_ADDRESS3)

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
    input_max1 = upthreshold1
    input_max2 = upthreshold2
    input_max3 = upthreshold3
    output_min = 100 #frequency in hz, higher is faster pumping
    output_max = MAX_MOTOR_SPEED
    
    # Calculate the ratio
    ratio1 = (output_max - output_min) / (input_max1 - input_min)
    ratio2 = (output_max - output_min) / (input_max2 - input_min)
    ratio3 = (output_max - output_min) / (input_max3 - input_min)
    #print(ratio)
        
    global BloodLost
    BloodLost = 0 
    liquid = l

    #---------------------------------------------------
    #name file to save data to
    '''name = input ("enter trial run name")
    filename=(f"{name}.txt")'''
    filename = (f"A - Previous Trial.txt")
    #Throw error codes for when and if there is something that can't be in a file name and have them try again
    open(filename,"w")
    #add header---------------------
    print (filename)
    #Create empty lists
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    #---------------------------------------------------

    global Hz, totaltime
    p=GPIO.PWM(PUL, 100)   #PWM Function is defined
    #GPIO.output(18, 1)     #Open Solenoid
    p.start(0)             #PWM is activated at a duty cycle of 0
    #Set loop count variable
    L=1
    tic3 = 0 #timestamp
    totaltime = 0
    print('1')
    cycletime = 0
    tic1 = time.perf_counter()
    
#---------------------------------------    
    #def open_sim_window():
    sim_window = Toplevel(root)
    sim_window.title("Simulation")
    #sim_window.geometry("1024x600")
    sim_window.configure(bg="grey75")
    sim_window.attributes("-zoomed", True)  # Maximizes the window
    #sim_window.attributes("-fullscreen", True)  # substitute `Tk` for whatever your `Tk()` object is called
    sleep(.5)    
    simlabelframe = LabelFrame(sim_window, padx=50, pady=5,fg="black", bg="gray75")
    simlabelframe.grid(row=0, column=0,pady=10, padx=45)
       
    # Add a label at the top of the window
    label_simulation = Label(simlabelframe, text="Simulation", font=("Arial", largetitletext), fg="black", bg="gray75")
    label_simulation.grid(row=0, column=0, pady=5,padx=10)
        #Add left frame
    updatesframe = LabelFrame(sim_window,bg="firebrick3", fg="white")
    updatesframe.grid(row=1, column=0)
        #Add Middle frame
    graphframe = LabelFrame(sim_window,bg="firebrick3", fg="white")
    graphframe.grid(row=0, column=1, rowspan=2)    
        #Add bottom Frame
    bleedoutbarframe = LabelFrame(sim_window,bg="firebrick3", fg="white")
    bleedoutbarframe.grid(row=2,columnspan = 2, column=0)


    # Add the updates section label
    label_updates = Label(updatesframe, text="Updates", bg="firebrick3", fg="white", font=("Arial", mediumtitletext), anchor='ne')
    label_updates.grid(row=0, column=0)
    # Create text widget and specify size.
    T = Text(updatesframe, height = 14.35, width = 37, bg="white",font=("Arial", smalltext))
    T.grid(row=1, column=0)
    T.insert(END, "Get Started, He is losing blood fast!")
    # Add the frame hat the graph will go in
    label_graph = Label(graphframe, text="graph", bg="firebrick3", fg="white",font=("Arial", smalltext))
    label_graph.grid(row=0, column=0)     
    # Add the frame that the bleedout bar will go in
    label_bleedoutbar = Label(bleedoutbarframe, text="Bleedoutbar", bg="firebrick3", fg="white", font=("Arial", mediumtitletext), padx=10, pady=10)
    label_bleedoutbar.grid(row=0, column=0, sticky="w")
    label_home = Label(graphframe, text="Pressure On Wound", font=("Arial", mediumtitletext), fg="white", bg="firebrick3", padx=10, pady=10)
    label_home.grid(row=0, column=0)
        

    fig = Figure(figsize=(12, 7.2))        
    x = []
    m = []
    ma_x = []
        
    ax = fig.add_subplot(111)
    line, = ax.plot(x, m)
    line_20ref, = ax.plot(x, ma_x)
    
    # Add the canvas for the graph
    canvas_graph = FigureCanvasTkAgg(fig, master=graphframe)  # A tk.DrawingArea.
    canvas_graph.draw()
    canvas_graph.get_tk_widget().grid(row=1,column=0)
    
#-----------------------------------------------------------    
    def updates(b,p):
        global x1, x2, x3, x4, x5, x6, x7, x8
    
        if b >= .25 and x1 == 0:
            T.insert(END,"\n" + "Get Started, He is losing blood fast!1")
            help_me2.play()
            x1=1
        if b >= .5 and x2 == 0:
            T.insert(END,"\n" + "Get some pressure on this wound.")
            x2=1
        if b >= 1.5 and x3 == 0:
            T.insert(END,"\n" + "Hurry, he has lost half of his blood.")
            x3=1    
        if b >= 2.5 and x4 == 0:
            T.insert(END,"\n" + "You are running out of time to save him.")
        
        
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
            T.insert(END,"\n" + "Make sure to pack the wound very tightly.")
            x6=1
        if p >= 15 and x7 == 0 and method == 1:
            scream4.play()            
            T.insert(END,"\n" + "Put a bit more pressure on the wound.")
            x7=1    
        if p >= 2.5 and x8 == 0:
            T.insert(END,"\n" + "Don't listen to him, you need to focus on stopping the bleed.")
            gasp1.play()
            x8=1
    def failmessage() :
        you_failed.play()
        sleep(5)
        
    def successmessage():
        you_succeded.play()
        sleep(5)
        
    def bleedoutbar(b):    
        p = ttk.Progressbar(bleedoutbarframe, orient="horizontal", length=1915, mode="determinate",takefocus=True, maximum=3)       
        p['value'] = b
        p.grid(row=1, column=0, ipady=30)
        #root.after(20, bleedoutbar)
        
    def graph_function(t, d):
            
        ma_x = []
        x = t #[]
        m = d #[]
        
        #time = t
        #data = d
        
        #x.append(time)
        #m.append(data)
        ma_x.append(20)
        line.set_data(x, m)
        line_20ref.set_data(x, ma_x)
        ax.relim()  # Recalculate the limits of the plot
        ax.autoscale_view()  # Auto-scale the plot
        canvas_graph.draw()
        #root.after(20, graph_function)  # Schedule the next update after 1000ms (1 second)





    #Junction Wound #1
    while method == 1 :
        #This Turns Relay On.(opens solenoid) 
        GPIO.output(junction, 1)
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
                            GPIO.output(junction, 0) 
                            quit()  
     #---------------------------------------
            #Raw Data is turned into lbs and filtered
        LBS_DATA_SENSOR1=((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
        print ("Sensed load = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000), "pounds")#plots out       
        LBS_DATA_SENSOR1 = 1.5 * LBS_DATA_SENSOR1
        if LBS_DATA_SENSOR1 < 0:
            LBS_DATA_SENSOR1 = 0
        if LBS_DATA_SENSOR1 > 0 and LBS_DATA_SENSOR1 <= upthreshold1:  #upthreshpld line 300  
            STB_timer=0
        if LBS_DATA_SENSOR1 > upthreshold1 and LBS_DATA_SENSOR1 <= 40:
            LBS_DATA_SENSOR1 = upthreshold1
            STB_timer = STB_timer + cycletime
            if STB_timer >= 6:#how to actually stop the bleed
                print('You Stopped The Bleed!!!')
                GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
                GPIO.output(junction, 0)
                #you_succeded.play()
                success = threading.Thread(target=successmessage)
                success.start()
                sleep(5)
                quit()            
        if LBS_DATA_SENSOR1 > 40:
            LBS_DATA_SENSOR1 = 0 
        print('filtered data:', LBS_DATA_SENSOR1, 'Pounds')
        
    #---------------------------------------
        Hz = -(LBS_DATA_SENSOR1) * ratio1 + output_max
        print(Hz)
    #---------------------------------------
        if liquid == 1:
            #This Turns Relay On. 
            GPIO.output(junction, 1)
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
            GPIO.output(junction, 0)#turn off solenoid
            you_failed.play()
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
        with open(filename, "a") as file:
            #for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{totaltime}\t{BloodLost}\t{LBS_DATA_SENSOR1}\n")
    #---------------------------------------            
        #Update Graph(pop up graph)
        if LBS_DATA_SENSOR1 > running_max:
            running_max = LBS_DATA_SENSOR1
           
        plt.plot(data1,data3,'b-', linewidth=2)
        plt.xlim(totaltime-15, totaltime+15)
        plt.ylim(0, running_max + 10)
        plt.pause(0.1)
        
        graph_function(data1, data3)
        
    #----------------------------------------
        bleedoutbar(BloodLost)
    #----------------------------------------
        x = threading.Thread(target=updates, args=(BloodLost,LBS_DATA_SENSOR1))
        x.start()
        #updates(BloodLost,LBS_DATA_SENSOR1)
    #---------------------------------------       
        #time refrence at the end of the cycle
        tic5 = time.perf_counter()
        totaltime = tic5-tic1
        print (totaltime)
        
        #graph_function(totaltime, LBS_DATA_SENSOR1)
    #---------------------------------------     

        #Count the times through the loop
        L+=1
        print('Loopcount =', L)
    #---------------------------------------   
     








    #Tourniquet (2)
    while method == 2 :
        #This Turns Relay On.(opens solenoid) 
        GPIO.output(arm, 1)
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
                            GPIO.output(ENA, GPIO.HIGH) #stop motor
                            GPIO.output(arm, 0)
                            quit()  
     #---------------------------------------
            #Raw Data is turned into lbs and filtered
        LBS_DATA_SENSOR2=((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
        print ("Sensed load2 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000), "pounds")#plots out
        LBS_DATA_SENSOR3=((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
        print ("Sensed load3 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000), "pounds")#plots out
        
        TOTAL_LBS= .5 * (2*LBS_DATA_SENSOR2+.75*LBS_DATA_SENSOR3)
        TOTAL_LBS = TOTAL_LBS - 1
     
          #Ratio of load cell data to calcualte where the weight is
        
        distribution = LBS_DATA_SENSOR2/(LBS_DATA_SENSOR2+LBS_DATA_SENSOR3)
        if distribution  < .5:
            print('Apply Tourniquet higher on arm')
     
        if TOTAL_LBS < 0:
            TOTAL_LBS = 0
            TOTAL_LBS_FILTERED = 0
        if TOTAL_LBS > 0 and TOTAL_LBS <= upthreshold2:    
            TOTAL_LBS_FILTERED = TOTAL_LBS
            STB_timer=0
        if TOTAL_LBS > upthreshold2 and TOTAL_LBS <= 80:
            TOTAL_LBS_FILTERED = upthreshold2
            if distribution > .5:
                STB_timer = STB_timer + cycletime
                if STB_timer >= 6:
                    print('You Stopped The Bleed!!!')
                    GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
                    GPIO.output(4, 0)
                    sleep(.1)
                    you_succeded.stop()
                    sleep(1)
                    you_succeded.play()
                    sleep(5)
                  
                    quit()
            
        if TOTAL_LBS > 80:
            TOTAL_LBS_FILTERED = 0 
        print('filtered data:',TOTAL_LBS_FILTERED, 'Pounds')
        
    #---------------------------------------

        
        
        
        
        
        
    #---------------------------------------
        Hz = -(TOTAL_LBS_FILTERED) * ratio2 + output_max
        print(Hz)
    #---------------------------------------
        if liquid == 1:
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
            GPIO.output(arm, 0)#turn off solenoid
            you_failed.play()
            sleep (5)
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
        with open(filename, "a") as file:
            #for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{totaltime}\t{BloodLost}\t{TOTAL_LBS}\n")
        
    #---------------------------------------            
        #Update Graph(pop up graph)      
                   
        if TOTAL_LBS > running_max:
            running_max = TOTAL_LBS
        plt.plot(data1,data3,'b-', linewidth=2)
        plt.xlim(0, totaltime+15)
        plt.ylim(0, running_max + 10)
        plt.pause(0.1)
        
        graph_function(data1, data3)



        bleedoutbar(BloodLost)
    #----------------------------------------
        updates(BloodLost,TOTAL_LBS)        
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







    #Direct Pressure (3)
    while method == 3  :
        #This Turns Relay On.(opens solenoid) 
        GPIO.output(arm, 1)
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
                            GPIO.output(ENA, GPIO.HIGH) #stop motor
                            GPIO.output(arm, 0)
                            quit()  
     #---------------------------------------
            #Raw Data is turned into lbs and filtered
        LBS_DATA_SENSOR2=((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
        print ("Sensed load2 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000), "pounds")#plots out
        LBS_DATA_SENSOR3=((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
        print ("Sensed load3 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000), "pounds")#plots out
        
        TOTAL_LBS= .5 * (LBS_DATA_SENSOR2+LBS_DATA_SENSOR3)
        TOTAL_LBS = TOTAL_LBS - 1
     
          #Ratio of load cell data to calcualte where the weight is
        

        if TOTAL_LBS < 0:
            TOTAL_LBS = 0
            TOTAL_LBS_FILTERED = 0
        if TOTAL_LBS > 0 and TOTAL_LBS <= upthreshold3:    
            TOTAL_LBS_FILTERED = TOTAL_LBS
            STB_timer=0
        if TOTAL_LBS > upthreshold3 and TOTAL_LBS <= 100:
            TOTAL_LBS_FILTERED = upthreshold3
            STB_timer = STB_timer + cycletime
            if STB_timer >= 6:
                print('You Stopped The Bleed!!!')
                GPIO.output(ENA, GPIO.HIGH) #turn off enable so motor turns off
                GPIO.output(4, 0)
                you_failed.play()
                sleep(5)
                quit()
            
        if TOTAL_LBS > 80:
            TOTAL_LBS_FILTERED = 0 
        print('filtered data:',TOTAL_LBS_FILTERED, 'Pounds')
        
    #---------------------------------------

        
        
        
        
        
        
    #---------------------------------------
        Hz = -(TOTAL_LBS_FILTERED) * ratio3 + output_max
        print(Hz)
    #---------------------------------------
        if liquid == 1:
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
            GPIO.output(arm, 0)          #turn off solenoid
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
        with open(filename, "a") as file:
            #for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{totaltime}\t{BloodLost}\t{TOTAL_LBS}\n")
        
    #---------------------------------------            
        #Update Graph(pop up graph)      
                   
        if TOTAL_LBS > running_max:
            running_max = TOTAL_LBS
        plt.plot(data1,data3,'b-', linewidth=2)
        plt.xlim(0, totaltime+15)
        plt.ylim(0, running_max + 10)
        plt.pause(0.1)
        
        graph_function(data1, data3)



        bleedoutbar(BloodLost)
    #----------------------------------------
        updates(BloodLost,TOTAL_LBS)        
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


'''

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
        if liquid == 1:
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
            #for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{totaltime}\t{BloodLost}\t{LBS_Sensor3}\n")
    #---------------------------------------            
        #Update Graph
        if LBS_DATA_SENSOR3 > running_max:
            running_max = LBS_DATA_SENSOR3
        plt.plot(data1,data3,'b-', linewidth=2)
        plt.xlim(0, totaltime+15)
        plt.ylim(0, running_max + 10)
        plt.pause(0.1)
        
        graph_function(data1, data3)
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
'''
root.mainloop()


