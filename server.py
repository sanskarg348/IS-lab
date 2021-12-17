import socket
from cryptography.fernet import Fernet
from os import system
import time

def runServeo(p):
    print("Connecting to External network....")
    system(f'ssh -R {p}:0.0.0.0:{p} serveo.net > /dev/null &')
    time.sleep(5)
    ip = socket.gethostbyname('serveo.net')
    print(f"IP: {ip} \t PORT: {p}")
    print("Share the above IP and PORT number with client.")




print("Socket successfully created")
# server_name = input('Enter the server you want to use: ')
port = int(input('Enter the port you wanna use: '))
runServeo(port)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('0.0.0.0', port))
print("socket binded to %s" %port)
s.listen(5)
key = Fernet.generate_key()
fernet = Fernet(key)



def chat(c, f):
    name_server = input('Name: ')
    g = f.decrypt(c.recv(1024)).decode()
    c.send(f.encrypt(name_server.encode()))
    client = g
    g = f.decrypt(c.recv(1024)).decode()
    while g != 'bye':
        print(f'{client}: {g}')
        msg = input(f"{name_server}: ")
        c.send(f.encrypt(msg.encode()))
        g = f.decrypt(c.recv(1024)).decode()


c, addr = s.accept()
system('clear')
print('Got connection from', addr)
c.send(key)
chat(c, fernet)
c.close()

