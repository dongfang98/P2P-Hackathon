from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Frame
from tkinter import Button
from tkinter import LEFT
from tkinter import END
class WindowLogin(Tk):
    #login window
    def __init__(self):
        super(WindowLogin,self).__init__()
        #set the property of window
        #set the title of the window by using the parent function

        self.window_init()
        #Fill control
        #add a widget as a child
        self.add_widgets()
    def window_init(self):
        self.title('Login')
        #set size and position(widthXheight+X+Y)
        
        self.geometry('255x95+460+230')
        #set whether window can be stretched
        
        self.resizable(False, False)
    def add_widgets(self):
        #username, call function in the class
       

        username_label= Label(self)
        #user_label is the dictionary object, text and key is value and name of user_label

        username_label['text']='Username:'
        #set the position of window, pad is edge distance and grid is function of Label

        username_label.grid(row=0,column=0,padx=10,pady=5)
        #set input box
        username_entry=Entry(self,name='username_entry')
        #username_entry is also a dictionary, width = 22 means that max char input is 22

        username_entry['width']=22
        username_entry.grid(row=0, column=1)

        # password
        password_label = Label(self)
        password_label['text'] = 'Password:'
        password_label.grid(row=1, column=0, padx=10, pady=1)
        # set input box
        password_entry = Entry(self, name='password_entry')
        password_entry['width'] = 22
        #use '*' to cover the password
        password_entry['show'] ='*'
        password_entry.grid(row=1, column=1)

        #use frame mode to create button, which means devide a part of the second line in grid to frame
        #so that we can set button at the mid of area

        ####Now, through function init, self become  a window(an area) and Framen is a sub area in self 
        ####button is a sub area in button_frame


        #This Frame is a fixed format，
        button_frame=Frame(self,name='button_frame')
        button_frame.grid(row=2,columnspan=2,pady=5)
        #call button class
        reset_button=Button(button_frame,name='reset_button')
        reset_button['text']='Reset'

        #there are two buttons in the frame, both pack and grid process layout.
        #tkinter has three layout managers that use geometric methods to 
        # position widgets in an app frame: pack,place, grid
        #pack method declares the position of widget in relation to each other
        reset_button.pack(side=LEFT,padx=10)

        #login button
        login_button = Button(button_frame, name='login_button')
        login_button['text'] = 'Login'
        login_button.pack(side=LEFT)

    def on_login_button_click(self,command):
        #use['command'] to set function to button, we use children to search beacuse button is a local variable

        #chileren is a sub function of TK, tyope is a dictionary. We can use name to search a sub area

        login_button = self.children['button_frame'].children['login_button']
        login_button['command']=command
    def on_reset_button_click(self,command):
        reset_button=self.children['button_frame'].children['reset_button']
        reset_button['command']=command
    def get_username(self):
        #get input in username inputbox

        return self.children['username_entry'].get()
    def get_password(self):
        return self.children['password_entry'].get()
    def clear_username(self):
        #clear the input box

        self.children['username_entry'].delete(0,END)
    def clear_password(self):
        self.children['password_entry'].delete(0, END)
    def on_window_close(self,command):
        # use built-in fucntion to release resource after close the window
        #this line means click button to excute this command

        self.protocol('WM_DELETE_WINDOW',command)
if __name__ =='__main__':
   window=WindowLogin()
   window.mainloop()