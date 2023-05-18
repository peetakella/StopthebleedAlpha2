import time
import sys
import RPi.GPIO as GPIO
import tkinter as tk
import tkinter.font as font
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import numpy
from sys import exit
from hx711 import HX711
from statistics import median

calibration_weight=15.6

fast_speed = 25000
slow_speed = 2000
stop_sensitivity = .9
stop_override = 0.5
teams = []
ready = 1
estop = 0

PUL = 12  # Stepper Drive Pulses
DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
hx = HX711(5,6)
hx.set_reading_format("MSB", "MSB")


GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
p = GPIO.PWM(PUL,fast_speed)
p.start(50)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

def down():
    global fast_speeed
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(DIR, GPIO.LOW)
    p.ChangeFrequency(fast_speed)
    return
#
#
def up():
    global fast_speed
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(DIR, GPIO.HIGH)
    p.ChangeFrequency(fast_speed)
    return

def upSlow():
    global slow_speed
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(DIR, GPIO.HIGH)
    p.ChangeFrequency(slow_speed)
    return

def stop():
    global estop
    GPIO.output(ENA, GPIO.LOW)
    estop = 1
    return

def close():
    GPIO.cleanup()
    win.destroy()
    exit()
    
def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def populate(frame):
    for row in range(0,99):
        tk.Label(frame, text=str(row+1), width=3, borderwidth="1",
                 relief="solid",background="white",
                 font=smallfont).grid(row=row, column=0,sticky="nsew")
        tk.Label(frame, width=27, borderwidth="1",
                 relief="solid",background="white",
                 font=smallfont).grid(row=row, column=1,sticky="nsew")
        tk.Label(frame, width=7, borderwidth="1",
                 relief="solid",background="white",
                 font=smallfont).grid(row=row, column=2,sticky="nsew")
        
def update(f):
    global tdata, fdata, line, starttime
    t = time.time()-starttime
    tdata.append(t)
    fdata.append(f)
    line.set_data(tdata, fdata)
    ax.set_xlim(right=max(tdata)*1.05)#stretches axis for data
    ax.set_ylim(top=max(fdata)*1.05)
    return line,ax

def getLoad():
    global stop_sensitivity, stop_override
    while (fdata[-1]>fdata[-2]*stop_sensitivity or fdata[-2]<stop_override) and not estop:
        yield hx.get_weight(1)
        time.sleep(0.05)
    crush2()
        
def crush():
    global tdata, fdata, line, ready, estop, starttime
    if ready == 1:
        tk.messagebox.showwarning("Invalid Operation","Not ready to crush yet, please input another team first.")
        return
    else:
        estop = 0
        ready = 1
        hx.reset()
        hx.tare() #sets current voltage to zero point
        tdata = [0,0]
        fdata = [0,0]
        line = Line2D(tdata, fdata)
        line.set_animated(True)
        fig.clear()
        ax.add_line(line)
        starttime=time.time()
        ani = FuncAnimation(fig, update, getLoad, interval=5,blit=True,repeat=False)
        
        win.update()
        upSlow()
    return

def crush2():
    global teams, fdata
    stop()
    teams[-1][1] = round(max(fdata),2)
    updateTeams()
    return
    
def newTeam():
    global teams, ready, frame, win
    if ready:
        name = tk.simpledialog.askstring("Input","What is your team name?",parent=win)
        if(name is None or name == ''):
            return
        else:
            teams.append([name,0])
            tk.Label(frame, text=teams[-1][0],width=27, borderwidth="1",
                     relief="solid",background="white",
                     font=smallfont).grid(row=len(teams)-1, column=1,sticky="nsew")
            tk.Label(frame, width=7, text=str(teams[-1][1]), borderwidth="1",
                 relief="solid",background="white",
                 font=smallfont).grid(row=len(teams)-1, column=2,sticky="nsew")
            win.update()
            ready = 0
    else:
        tk.messagebox.showwarning("Invalid Operation","The last team added hasn't gone yet! Either crush a truss, or delete a team.")
    return

def updateTeams():
    global teams
    teams.sort(key=lambda x:x[1])
    teams.reverse()
    for i in range(len(teams)):
        tk.Label(frame, width=27, text=teams[i][0], borderwidth="1",
                 relief="solid",background="white",
                 font=smallfont).grid(row=i, column=1,sticky="nsew")
        tk.Label(frame, width=7, text=str(teams[i][1]), borderwidth="1",
                 relief="solid",background="white",
                 font=smallfont).grid(row=i, column=2,sticky="nsew")
    win.update()

def delTeam():
    global ready, teams
    num = tk.simpledialog.askinteger("Input","Which position team do you wish to delete?",parent=win)
    if num is None:
        return
    elif num <= 0:
        tk.messagebox.showwarning("Invalid Operation","Come on, at least put in a number that COULD be assigned to a team!")
        return
    try:
        a = teams[num-1]
    except:
        tk.messagebox.showwarning("Invalid Operation","There aren't even that many teams!")
    else:
        teams.pop(num-1)
        updateTeams()
        tk.Label(frame, width=27, borderwidth="1",
                 relief="solid",background="white",
                 font=smallfont).grid(row=len(teams), column=1,sticky="nsew")
        tk.Label(frame, width=7, borderwidth="1",
                 relief="solid",background="white",
                 font=smallfont).grid(row=len(teams), column=2,sticky="nsew")
        ready = 1
    return

def calibrate():
    global calibration_weight
    tk.messagebox.showinfo("Calibrating...","Remove all weight from the crusher and then press OK.")
    hx.tare()
    tk.messagebox.showinfo("Calibrating...","Place the calibration weight on the crusher and then press OK.")
    weight = hx.get_weight(25)
    hx.set_reference_unit(weight/calibration_weight)
    tk.messagebox.showinfo("Calibrated","Calibration done!")
    

win = tk.Tk()
win.attributes('-fullscreen', True)
win.title('It\'s Truss Crushing Time!')
bigfont = font.Font(size=100)
medfont = font.Font(size=18)
smallfont = font.Font(size=14)

fig, ax = plt.subplots()
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
upbtn = tk.Button(win, text="Up",command=up,font=medfont,width=4,background="cyan")
downbtn = tk.Button(win, text="Down",command=down,font=medfont,width=4,background="cyan")
stopbtn = tk.Button(win, text="Stop",command=stop,font=medfont,width=4,background="red")
crushbtn = tk.Button(win, text="CRUSH!",command=crush,font=bigfont,background="green")
closebtn = tk.Button(win, text="X",width=1,height=1,command=close,background="red",font=smallfont)
newbtn = tk.Button(win, text="New Team",command=newTeam,font=medfont)
delbtn = tk.Button(win, text="Delete Team",command=delTeam,font=medfont)

upbtn.grid(row=3,column=1,padx=20,pady=20,sticky="nws")
downbtn.grid(row=3,column=1,padx=20,pady=20,sticky="nes")
stopbtn.grid(row=3,column=1,padx=20,pady=20,sticky="ns")
crushbtn.grid(row=2,column=0,columnspan=3,padx=20,pady=10,sticky="news")
closebtn.grid(row=0,column=6,padx=5,pady=5,sticky=tk.N+tk.E)
newbtn.grid(row=3,column=3,padx=20,pady=20,sticky="news")
delbtn.grid(row=3,column=4,padx=20,pady=20,sticky="news")

graph = FigureCanvasTkAgg(fig, win)
graph.get_tk_widget().grid(row=0,column=0,rowspan=2,columnspan=3,padx=20,pady=20,sticky="news")

canvas = tk.Canvas(win, borderwidth=0,background="white")
frame = tk.Frame(canvas,background="white")
vsb = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
vsb.grid(row=1,column=5,rowspan=2,sticky="nws")
canvas.grid(row=1,column=3,rowspan=2,columnspan=2,pady=10,sticky="news")
canvas.create_window((4,4),window=frame,anchor="nw")
frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

tk.Label(win,text="Team Name      ",font=medfont).grid(row=0,column=3,columnspan=2,sticky="s")
tk.Label(win,text="Load  ",font=medfont).grid(row=0,column=4,sticky="se")
tk.Label(win,text="Crushing Progress",font=font.Font(size=24),background="white").place(in_=graph.get_tk_widget(),relx=0.513,rely=0.086,anchor="center")
tk.Label(win,text="Time (s)",font=medfont,background="white").place(in_=graph.get_tk_widget(),relx=0.513,rely=0.955,anchor="center")
txtcanv = tk.Canvas(win,width=40,height=120,background="white",highlightthickness=0)
txtcanv.place(in_=graph.get_tk_widget(),relx=0.075,rely=0.51,anchor="center")
txtcanv.create_text(20,60,text="Load (lbf)",angle=90,font=medfont)


win.columnconfigure(0, weight=5)
win.columnconfigure(1, weight=5)
win.columnconfigure(2, weight=5)
win.columnconfigure(3, weight=4)
win.columnconfigure(4, weight=4)
win.columnconfigure(5, weight=1)
win.columnconfigure(6, weight=1)
win.rowconfigure(0, weight=1)
win.rowconfigure(1, weight=20)
win.rowconfigure(2, weight=5)
win.rowconfigure(3, weight=5)

populate(frame)

win.after(1000,calibrate)
win.mainloop()



GPIO.cleanup()

