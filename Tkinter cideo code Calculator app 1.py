from tkinter import *

root = Tk()
root.title("Simple Calculator")

e = Entry(root, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan=4, padx=5,pady=10)

def Button_click(number):
    
    current = str(e.get())+ str(number)
    e.delete(0,END)
    e.insert(0,current)
    

def Button_add():
    first_number = e.get()
    global fnum
    global math
    math = "add"
    fnum = int(first_number)
    e.delete(0,END)
   
def Button_equal():
    second_number = e.get()
    e.delete(0,END)
    
    if math == "add":
        e.insert(0,fnum + int(second_number))
    if math == "subtract":
        e.insert(0,fnum - int(second_number))
    if math == "multiply":
        e.insert(0,fnum * int(second_number))
    if math == "devide":
        e.insert(0,fnum / int(second_number))
    
def Button_subtract():
    first_number = e.get()
    global fnum
    global math
    math = "subtract"
    fnum = int(first_number)
    e.delete(0,END)
    
def Button_multiply():
    first_number = e.get()
    global fnum
    global math
    math = "multiply"
    fnum = int(first_number)
    e.delete(0,END)
    
def Button_devide():
    first_number = e.get()
    global fnum
    global math
    math = "devide"
    fnum = int(first_number)
    e.delete(0,END)    

def Button_clear():
    e.delete(0,END)

button0=Button(root,text="0",width=5, padx=7,command=lambda:Button_click(0)).grid(row=4,column=0)
button1=Button(root,text="1",width=5, padx=7,command=lambda:Button_click(1)).grid(row=3,column=0)
button2=Button(root,text="2",width=5, padx=7,command=lambda:Button_click(2)).grid(row=3,column=1)
button3=Button(root,text="3",width=5, padx=7,command=lambda:Button_click(3)).grid(row=3,column=2)
button4=Button(root,text="4",width=5, padx=7,command=lambda:Button_click(4)).grid(row=2,column=0)
button5=Button(root,text="5",width=5, padx=7,command=lambda:Button_click(5)).grid(row=2,column=1)
button6=Button(root,text="6",width=5, padx=7,command=lambda:Button_click(6)).grid(row=2,column=2)
button7=Button(root,text="7",width=5, padx=7,command=lambda:Button_click(7)).grid(row=1,column=0)
button8=Button(root,text="8",width=5, padx=7,command=lambda:Button_click(8)).grid(row=1,column=1)
button9=Button(root,text="9",width=5, padx=7,command=lambda:Button_click(9)).grid(row=1,column=2)
buttonplus=Button(root,text="+",width=5, padx=7, command=Button_add).grid(row=1,column=3)
buttonminus=Button(root,text="-",width=5, padx=7, command=Button_subtract).grid(row=1,column=4)
buttontimes=Button(root,text="*",width=5, padx=7, command=Button_multiply).grid(row=2,column=3)
buttondevide=Button(root,text="/",width=5, padx=7, command=Button_devide).grid(row=2,column=4)
buttonequals=Button(root,text="=",width=13, padx=9, pady=15, command=Button_equal).grid(row=3,column=3,columnspan=2,rowspan=2)
buttonclear=Button(root,text="Clear", width=13,padx=9, command=Button_clear).grid(row=4,column=1,columnspan=2)

root.mainloop()