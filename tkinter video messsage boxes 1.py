from tkinter import *
from tkinter import messagebox
root = Tk()
root.title('message boxes')



def popup():
    variablename = messagebox.askyesno("This is my Popup!", "Hello World!")
#   messagebox.[type of box](showinfo, showwarning,showerror, askquestion, askokcancel, askyesno)(Title, text)
    label = Label(root, text=variablename).pack()
    if variablename == 1:
        Label(root, text="you clicked yes").pack()
    else    :
        Label(root, text="you clicked no").pack()
        
button1 = Button(root, text="popup", command = popup).pack()


root.mainloop()