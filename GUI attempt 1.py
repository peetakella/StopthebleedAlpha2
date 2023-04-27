from tkinter import *


root = Tk()
root.title("frame")

root.geometry("500x500")

frame1 = LabelFrame(root,padx=100, pady=50)
frame1.grid(row=0, column=0, columnspan=2, padx=50, pady=25)

label_1 = Label(frame1, text="Stop The Bleed",font=('Times',24))
label_1.pack()


def Setup():
    Win1 = Toplevel()
    #global my_label
    #sometimes you have to call thins out as global variables to get them to work in new windows
    Win1.title("Choose Scenereo")
    Win1.geometry("500x500")
    
    Win1frame1 = LabelFrame(Win1,padx=100, pady=50)
    Win1frame1.grid(row=0, column=0, columnspan=3, padx=50, pady=25)

    label_1 = Label(Win1frame1, text="Stop The Bleed 2",font=('Times',24))
    label_1.pack()
    
    Win1frame2 = LabelFrame(Win1,padx=15, pady=50)
    Win1frame2.grid(row=1, column=0, columnspan=1, padx=5, pady=25)
    
    label_1 = Label(Win1frame2, text="Stop The Bleed",font=('Times',12))
    label_1.pack()
    
    Win1frame3 = LabelFrame(Win1,padx=15, pady=50)
    Win1frame3.grid(row=1, column=1, columnspan=1, padx=5, pady=25)
    
    label_1 = Label(Win1frame3, text="Stop The Bleed",font=('Times',12))
    label_1.pack()
    
    Win1frame4 = LabelFrame(Win1,padx=15, pady=50)
    Win1frame4.grid(row=1, column=2, columnspan=1, padx=5, pady=25)
    
    label_1 = Label(Win1frame4, text="Stop The Bleed",font=('Times',12))
    label_1.pack()
    
    
    
    
    my_label = Label(Win1, text="it worked").pack()
    win1button1=Button(Win1, text="press me", command=Setup).pack()
    win1button2=Button(Win1, text="Quit", command=Win1.destroy).pack()





def Data():

    Win2 = Toplevel()
    #sometimes you have to call thins out as global variables to get them to work in new windows
    top.title("View Data")
    my_label = Label(Win2, text="it worked").pack()
    WinButton(Win2, text="press me", command=Open2).pack()
    Button(Win2, text="Quit", command=top.destroy).pack()









button1 = Button(root, text="Choose Scenerio",pady=100, padx=25,font=('Times',13), command=Setup).grid(row=1, column=0, pady=30, padx=15)

button2 = Button(root, text="Retrieve Data",pady=100, padx=25,font=('Times',13), command=Data).grid(row=1, column=1, pady=30, padx=15)




root.mainloop()