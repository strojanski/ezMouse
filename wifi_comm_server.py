import socket
import threading

#bind_ip = '127.0.0.1'     # Listen on all addresses
bind_ip = socket.gethostbyname(socket.gethostname())
bind_port = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print(f"Listening on {bind_ip}:{bind_port}")

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"Received: {request}")
    client_socket.send(b"ACK!")
    client_socket.close()

while True:
    client, addr = server.accept()
    print("[*] Accepted connection from: {}:{}".format(addr[0], addr[1]))
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()