from multiprocessing import connection
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import plyer
from kivy.uix.screenmanager import ScreenManager, Screen
import socket
from multiprocessing.connection import Client
from threading import Thread

host_name = socket.gethostname()
host_ip = socket.gethostbyname(socket.gethostname())
server_ip = "88.200.89.206"
server_port = 4444

class SettingsScreen (Screen):
    pass

class MouseScreen (Screen):
    left_value = False
    right_value = False

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        t = Thread(target=self.connection_fun)
        t.daemon = True
        t.start()

    def setLeft (self, *args):
        self.left_value = True
    
    def resetLeft (self, *args):
        self.left_value = False
    
    def setRight (self, *args):
        self.right_value = True
    
    def resetRight (self, *args):
        self.right_value = False
    
    def connection_fun(self):
        print("")
        server_ip = "88.200.89.206"
        server_port = 4444
        has_data = True
        try:
            print(f"Attempting to connect to {server_ip}:{server_port}")
            address = (server_ip, server_port)
            connection = Client(address, authkey=b"password")
            print(f"Connection to {server_ip}:{server_port} successful")
            while has_data:
                try:
                    sensor_data = self.get_data()
                    connection.send(sensor_data)     
                    info = connection.recv()
                except ValueError as e:
                    print("Cant send this data")
        except socket.error as err:
            print(err)
            print("Cant connect")


    def get_data(self):
        try:
            sensor = plyer.accelerometer
            sensor.enable()
            return [sensor.acceleration, self.left_value, self.right_value]

        except Exception:
            return (self.left_value, self.right_value)
            #return "Could not enable accelerometer!"

class Mouse (App):
    def build (self):
        shitfScreen = ScreenManager()
        shitfScreen.add_widget(SettingsScreen(name="SettingsScreen"))
        shitfScreen.add_widget(MouseScreen(name="MouseScreen"))
        print("check")
        return shitfScreen
        


if __name__ == "__main__":
    Mouse().run()



