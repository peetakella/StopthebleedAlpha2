from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title('frame')

frame1 = LabelFrame(root, text= "this is my frame", padx=50, pady=5)
frame1.grid(row=0, column=0,padx=1,pady=100)

button1 = Button(frame1, text="don't click here")
button1.grid(row=0, column=0)
button2 = Button(frame1, text="don't click here")
button2.grid(row=1, column=1)

frame2 = LabelFrame(root, text= "this is my frame2", padx=50, pady=5)
frame2.grid(row=1, column=0,padx=1,pady=100)

button3 = Button(frame2, text="don't click here")
button3.grid(row=0, column=0)
button4 = Button(frame2, text="don't click here")
button4.grid(row=1, column=1)

root.mainloop()