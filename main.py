import kivy
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen , ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock
import socket
import threading


client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',55555))
my_name=""


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.mesg1=Label(font_size=35)
        self.mesg2=Label(font_size=35)
        self.mesg3=Label(font_size=35)
        layout.add_widget(self.mesg1)
        layout.add_widget(self.mesg2)
        layout.add_widget(self.mesg3)

        write=BoxLayout(orientation='horizontal')
        self.mes=TextInput(font_size=32)
        write.add_widget(self.mes)

        self.send=Button(text="send",font_size=40,size_hint=(0.3,1))
        self.send.bind(on_press=self.send_data)
        write.add_widget(self.send)
        layout.add_widget(write)

        self.add_widget(layout)
        # Start listening for data from the socket in a separate thread
        threading.Thread(target=self.listen_for_data, daemon=True).start()

    def listen_for_data(self):
        while True:
            # Receive data from the socket
            data = client.recv(1024)
            message = data.decode('ascii')
            #print(message)
        # Update the labels with the received message

            self.mesg1.text = self.mesg2.text
            self.mesg2.text = self.mesg3.text
            self.mesg3.text=message

            Clock.schedule_once(lambda dt: self.update_label(self.mesg1.text,self.mesg2.text,message))

    def update_label(self, message1, message2,message3):
        self.mesg1.text = message1
        self.mesg2.text = message2
        self.mesg3.text = message3
    def send_data(self, instance):
        message = self.mes.text
        send_out_mesg=f'{my_name}: {message}'
        client.send(send_out_mesg.encode("ascii"))
        self.mes.text = ''





class first(GridLayout, Screen):
    def __init__(self,**kwargs):
        super(first,self).__init__(**kwargs)
        self.cols=1

        self.add_widget(Label(text="Choose a username",font_size=45))
        self.username=TextInput(font_size=45,multiline=False)
        self.add_widget(self.username)


        # Create a BoxLayout to center the button
        box_layout = BoxLayout(orientation='vertical')
        self.add_widget(box_layout)

        # Create a Button and add it to the BoxLayout
        self.submit_button = Button(text="Submit", size_hint_y=None, height=150,font_size=32)
        box_layout.add_widget(self.submit_button)

        # Bind a callback function to the on_press event of the Button
        self.submit_button.bind(on_press=self.on_submit)

    def on_submit(self, instance):
        global my_name
        user_name=self.username.text
        my_name=user_name
        client.send(user_name.encode("ascii"))        

        # Switching screens.
        self.manager.current = 'second'

class Myapp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(first(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        return sm

if __name__=="__main__":
    Myapp().run()
