from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import Text
from tkinter import Button
from tkinter import END
from tkinter import UNITS
from time import localtime,strftime,time
#We cannot use class WindowChat(TK), beacuse only one root window is allowed 
#but we can have multiple top level window

class WindowChat(Toplevel):
  def __init__(self):
    super(WindowChat,self).__init__()
    self.geometry('795x505')
    self.resizable(False,False)
    #add module
    self.add_widget()
  def add_widget(self):
      #add module
      #chat area
      #create a area that can scroll,where a main window contain many small window
      chat_text_area = ScrolledText(self)
      chat_text_area['width']=110
      chat_text_area['height']=30
      #window have two row(input area and button), 
      #So the first row has to be aligned with the second row, columnspan=2
      
      chat_text_area.grid(row=0,column=0,columnspan=2)
      #'green' is a label, and sets its color to green. All text with this label is green

      chat_text_area.tag_config('green',foreground='green')
      chat_text_area.tag_config('system',foreground='red')
      #Then we should save this area in a dictionary like other area
      
      self.children['chat_text_area']=chat_text_area
      #input area
      chat_input_area=Text(self,name='chat_input_area')
      chat_input_area['width'] = 100
      chat_input_area['height'] = 7
      chat_input_area.grid(row=1,column=0,pady=10)
      #send area
      send_button=Button(self,name='send_button')
      send_button['text']='send'
      send_button['width']=5
      send_button['height']=2
      send_button.grid(row=1,column=1)
  def set_title(self,title):
      self.title("Welcome %s!" %title)
  def on_send_button_click(self,command):
      #click send button and excute function commend

      self.children['send_button']['command']=command
  def get_inputs(self):
      #get message in input area and send it to chat room
      #we can delete value of chat_inout_area to get and delete
      #because area is text module

      return self.children['chat_input_area'].get(0.0,END)
  def clear_input(self):
      #clear the input box

      self.children['chat_input_area'].delete(0.0,END)
  def append_message(self,sender,message):
      #add a mesage to chat area
      #first show who send it and show the message he send

      send_time = strftime('%Y-%m-%d %H:%M:%S',localtime(time()))
      send_info='%s:%s\n' % (sender,send_time)
      #position insert is end

      self.children['chat_text_area'].insert(END,send_info,'green')
      self.children['chat_text_area'].insert(END,' '+message+'\n')

      #Automatically scroll down the screen
      self.children['chat_text_area'].yview_scroll(3,UNITS)
  def on_window_close(self,command):
      #close the window and release the resource

      self.protocol('WM_DELETE_WINDOW',command)
if __name__ == '__main__':
    WindowChat().mainloop()