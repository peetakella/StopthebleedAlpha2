
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',width=50,height=20,anchor="center",
                                    command=self.quit)
        self.quitButton.grid()
        
app = Application()
app.master.title('Title of window')
app.mainloop()
        
https://www.youtube.com/watch?v=YXPyB4XeYLA
https://github.com/TomSchimansky/CustomTkinter






#def foo():
 #   print("You pressed the button!")    
  #  return
#win = tk.Tk()
#win.attributes('-fullscreen',False)
#btn1 = tk.Button(win,text="This is a button!",command=foo,width=50,height=50,anchor="center")
#btn1.grid(row=0,column=0,padx=50,pady=50)

#win.mainloop()