from tkinter import *

root = Tk()
root.title("window1")


def Open2():
    top = Toplevel()
    #sometimes you have to call thins out as global variables to get them to work in new windows
    top.title("Window 2")
    my_label = Label(top, text="it worked").pack()
    Button(top, text="press me", command=Open2).pack()
    Button(top, text="Quit", command=top.destroy).pack()

btn1 = Button(root, text= "Open window 2", command=Open2).pack()











root.mainloop()