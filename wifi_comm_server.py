import socket
from multiprocessing.connection import Listener
import time
import sys
import signal
#class Server:
#    def __init__()


listen_ip = socket.gethostbyname(socket.gethostname())
listen_port = 4444     

listener = Listener((listen_ip, listen_port), authkey=b'password')
print (f"Listening on {listen_ip}:{listen_port}")

print ("Ready to connect")

# Accept a connection
conn = listener.accept()

count = 0
start = time.time()
while True:
    msg = conn.recv()
    print(f"received: {msg}")
    
    reply = f"Received msg thx, {start - time.time()}"
    conn.send(reply)
    
    print(count)
    count += 1