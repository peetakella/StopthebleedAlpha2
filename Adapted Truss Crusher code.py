import time
import sys
import tkinter as tk
import tkinter.font as font
import matplotlib as mpl
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import numpy

win = tk.Tk()
win.title('It\'s Truss Crushing Time!')

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
    

fig, ax = plt.subplots()
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

graph = FigureCanvasTkAgg(fig, win)
graph.get_tk_widget().grid(row=0,column=0,rowspan=2,columnspan=3,padx=20,pady=20,sticky="news")

canvas = tk.Canvas(win, borderwidth=0,background="white")
frame = tk.Frame(canvas,background="white")

win.mainloop()
