from tkinter import * #For python 3 use: from Tkinter import *

root = Tk()
root.title("Fee Fie Foe Fum")
w = 1200
h = 1000

frame = Frame(root, width=w, height=h)
frame.pack()
button1 = Button(frame, text="Mercy!",font=("Arial", 50))
button1.place(x=.1*w, y=.05*h, height=.25*h, width=.8*w)
button2 = Button(frame, text="Justice!",font=("Arial", 100))
button2.place(x=.1*w, y=.35*h, height=.25*h, width=.8*w)
text1 = Label(text="Verdict:",font=("Arial", 30))
text1.place(x=.1*w, y=.725*h)
tbox1 = Text(frame)
tbox1.place(x=.25*w, y=.65*h, height=.25*h, width=.65*w)

root.mainloop()