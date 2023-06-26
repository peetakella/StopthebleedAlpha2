from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

x = []
m = []
xx = 0
ma_x = []

root = Tk()
root.wm_title("Embedding in Tk")

frame1 = LabelFrame(root, padx=50, pady=10, fg="black", bg="gray75")
frame1.grid(row=0, column=0, columnspan=2, pady=20, padx=25)

label_home = Label(frame1, text="Hemorrhage Control Trainer", font=("Arial", 50), fg="black", bg="gray75")
label_home.grid(row=0, column=0, pady=20, padx=10)

fig = Figure()
ax = fig.add_subplot(111)
line, = ax.plot(x, m)
line_20ref, = ax.plot(x, ma_x)

canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0)

import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
IO.setwarnings(False)           #do not show any warnings
IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
IO.setup(19,IO.OUT)           # initialize GPIO19 as an output, not important for the pressure sensor or load cell

import sys
import time
import smbus
from time import sleep
from time import perf_counter
bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
channel = 1          #select channel

LOAD_SENSOR_ADDRESS=0x28
dummy_command=0x00
offset=int((input("Enter offset value, default 1000:") or 1000))                                        #subtracts zero offset per data sheet, should be 1000
LOAD_SENSOR_DATA=bus.read_byte(LOAD_SENSOR_ADDRESS)#This apparently turns the load sensor on, only need it once

def update_plot_to_loadcell_data():
    global x, m, offset, LOAD_SENSOR_DATA, xx
    
    bus.write_byte(LOAD_SENSOR_ADDRESS,0x00)                                          #without this command, the status bytes go high on every other read
    LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
    data_translated = int(float('{0:.3f}'.format(((LOAD_SENSOR_DATA[0]&63)*2**8 + LOAD_SENSOR_DATA[1] - offset)*100/14000)))
    
    xx += 0.1 #will be t or time
    x.append(xx) #append time
    m.append(data_translated)
    ma_x.append(20)
    line.set_data(x, m)
    line_20ref.set_data(x, ma_x)
    ax.relim()  # Recalculate the limits of the plot
    ax.autoscale_view()  # Auto-scale the plot
    canvas.draw()
    root.after(100, update_plot_to_loadcell_data)  # Schedule the next update after 1000ms (1 second)

root.after(1000, update_plot_to_loadcell_data)  # Start the update loop after 1000ms (1 second)
root.mainloop()