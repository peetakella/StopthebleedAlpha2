from tkinter import *

root = Tk()


myLabel1 = Label(root, text="Hello World!")
myLabel2 = Label(root, text="Hello World 2!")
myLabel3 = Label(root, text="bone")
myLabel4 = Label(root, text="                                                      ")
myLabel1.grid(row=0,column=0)
myLabel2.grid(row=1,column=1)
myLabel3.grid(row=2,column=0)
myLabel4.grid(row=3,column=1)
#this is the same as that
#myLabel1 = Label(root, text="Hello World!").grid(row=0,column=0)
#myLabel2 = Label(root, text="Hello World 2!").grid(row=1,column=1)
#myLabel3 = Label(root, text="bone").grid(row=2,column=0)
#myLabel4 = Label(root, text="                                                       ").grid(row=3,column=1)

root.mainloop()