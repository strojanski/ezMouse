import socket
from multiprocessing.connection import Client

host_name = socket.gethostname()
host_ip = socket.gethostbyname(socket.gethostname())
ip = "88.200.89.206"
port = 4444

address = (ip , port)            
conn = Client(address, authkey = b'password')        
conn.send(b"PING")
print(conn.recv())