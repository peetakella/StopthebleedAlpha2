from tkinter import *

root = Tk()


Label1= Label(root,text="Enter your name below")
Label1.pack()

e = Entry(root,width=50,borderwidth=5, fg="green")
e.pack()
e.insert(0,"type here")


def myClick():
    Hello = "Hello " + e.get()
    myLabel = Label(root, text=Hello)
    myLabel.pack()



#myButton1 = Button(root, text="Click me")
myButton2 = Button(root, text="Enter", command=myClick)#note no () after myClick because it will run myClick automatically when the program is run and not when clicked

#myButton1.pack()
myButton2.pack()



root.mainloop()