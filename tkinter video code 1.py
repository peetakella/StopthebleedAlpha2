from tkinter import *
#root widget is the base of everything and it outlines the overarching window
root = Tk()

#creating everything in tkinter is a 2 step process. You have to define it and then put it up
# Here we are creating a label widget
myLabel = Label(root, text="Hello World!")
#Here we are shoving it on screen
#pack shoves something on the window in the first way possible
myLabel.pack()

#
root.mainloop()