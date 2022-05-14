from multiprocessing import AuthenticationError
import socket
from multiprocessing.connection import Client
import pandas as pd

class Connection:
    def __init__(self, server_ip="88.200.89.206", server_port=4444, password=b"password"):
        self.server_ip = server_ip
        self.server_port = server_port

        address = (server_ip, server_port)
        while True:
            try:
                print(f"Attempting to connect to {server_ip}:{server_port}")
                self.connection = Client(address, authkey=password)
                print(f"Connection to {server_ip}:{server_port} successful")
                break
            except socket.error as err:
                print(err)
        

    def send_data(self, data):
        #while True:
        try:
            # Send accelometer data
            self.connection.send(data)
            print("I am sending sensor data")
            pass
        except KeyboardInterrupt:
            pass
            #break

df = pd.read_csv("test1.csv")
print(df.head())


host_name = socket.gethostname()
host_ip = socket.gethostbyname(socket.gethostname())
server_ip = "88.200.89.206"
server_port = 4444
print("shape = ", df.shape)
#address = (server_ip , server_port)            
#conn = Client(address, authkey = b'password') 
#while (True):       
#    conn.send(b"I am client")
#    print(conn.recv())

data = list("Testing different data types")
connect = Connection(server_ip, server_port)
connection = connect.send_data(df)