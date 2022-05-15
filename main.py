from importlib.machinery import WindowsRegistryFinder
from multiprocessing import connection
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import plyer
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import socket
from multiprocessing.connection import Client
from threading import Thread
import pandas as pd

host_name = socket.gethostname()
host_ip = socket.gethostbyname(socket.gethostname())
server_ip = "88.200.89.206"
server_port = 4444

class SettingsScreen (Screen):
    def activate_accelerometer(self):
        sensor = plyer.accelerometer
        sensor.enable()

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
    
    def connection_fun(self, *args):
        server_ip = "88.200.89.206"
        #server_ip = "192.168.43.196"
        server_port = 4444
        has_data = True
        try:
            print(f"Attempting to connect to {server_ip}:{server_port}")
            address = (server_ip, server_port)
            connection = Client(address, authkey=b"password")
            print(f"Connection to {server_ip}:{server_port} successful")
            while has_data:
                try:
                    sensor_data = []
                    for i in range(50):
                        data_array = [self.get_data()[0],
                                      self.get_data()[1],
                                      self.get_data()[2],
                                      self.left_value, 
                                      self.right_value]
                        for i in range(3):
                            if data_array[i] == None:
                                data_array[i] = 0.1
                        sensor_data.append(data_array)
                        

                    df = pd.DataFrame(sensor_data, columns=['accX', 'accY', 'accZ', 'left_value', 'right_value'])
                    connection.send(df)     
                    info = connection.recv()
                except ValueError as e:
                    print("Cant send this data")
        except socket.error as err:
            print(err)
            print("Cant connect")



    def get_data(self):
        try:
            sensor = plyer.accelerometer
            print(sensor.acceleration)
            return sensor.acceleration

        except Exception:
            #return (self.left_value, self.right_value)
            return (None, None, None)
#            return (3.0, 0.0, 0.0)

class Mouse (App):
    def build (self):
        shitfScreen = ScreenManager()
        shitfScreen.add_widget(SettingsScreen(name="SettingsScreen"))
        shitfScreen.add_widget(MouseScreen(name="MouseScreen"))
        print("check")
        return shitfScreen
        


if __name__ == "__main__":
    Mouse().run()



