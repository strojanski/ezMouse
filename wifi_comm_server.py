import socket
from multiprocessing.connection import Listener
import time
import sys
import _thread
import signal

# TODO continuous transfer

def input_thread(list_of_inputs):
    input()
    list_of_inputs.append(True)

listen_ip = socket.gethostbyname(socket.gethostname())
listen_port = 4444     

listener = Listener((listen_ip, listen_port), authkey=b'password')
print (f"Listening on {listen_ip}:{listen_port}")

print ("Ready to connect")

# Accept a connection
conn = listener.accept()

run = True

count = 0
start = time.time()
list_of_inputs = []
_thread.start_new_thread(input_thread, (list_of_inputs,))
while not list_of_inputs:
    while conn.poll():
        try:
            msg = conn.recv()
            print(f"received: {msg}")
            
            conn.send(b"thx")
            
            print(count)
            count += 1
        except EOFError as err:
            run = False
