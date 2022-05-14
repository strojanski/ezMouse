import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from multiprocessing import AuthenticationError
import socket
from multiprocessing.connection import Client

host_name = socket.gethostname()
host_ip = socket.gethostbyname(socket.gethostname())
server_ip = "88.200.89.206"
server_port = 4444

#address = (server_ip , server_port)            
#conn = Client(address, authkey = b'password') 
#while (True):       
#    conn.send(b"I am client")
#    print(conn.recv())



class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1

        self.connect_btn = Button(text="connect")
        self.connect_btn.bind(on_press=self.connection_fun)
        self.add_widget(self.connect_btn)


    def connection_fun(self, instance):
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(socket.gethostname())
        server_ip = "88.200.89.206"
        server_port = 4444
        try:
            print(f"Attempting to connect to {server_ip}:{server_port}")
            self.connection = Client(address, authkey=password)
            print(f"Connection to {server_ip}:{server_port} successful")
        
        except socket.error as err:
            print(err)
        data = list("Testing different data types")
        #connection = connect.send_data(b"I am connecting (client)")


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
