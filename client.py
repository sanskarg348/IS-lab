import socket
from cryptography.fernet import Fernet
import tkinter
from os import system


def chat(c,f):
    def receive():
        msg = f.decrypt(c.recv(1024)).decode()
        msg_list.insert(tkinter.END, f"{server_name}: {msg}")

    def send(event=None):  # event is passed by binders.
        msg = my_msg.get()
        my_msg.set("")
        c.send(f.encrypt(msg.encode()))
        msg_list.insert(tkinter.END, f'{client_name}: {msg}')
        receive()
        if msg == 'bye':
            top.quit()
            return

    def on_closing(event=None):
        my_msg.set("bye")
        send()

    client_name = input('Enter your name: ')
    c.send(f.encrypt(client_name.encode()))
    server_name = f.decrypt(c.recv(1024)).decode()
    top = tkinter.Tk()
    top.title("Chatter")

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("Type your messages here.")
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
    msg_list.insert(tkinter.END, f"Greetings {client_name} If you ever feel like quiting send bye as a message ")
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)
    tkinter.mainloop()  # Starts GUI execution.


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
system('clear')
server_name = input('Enter the server name you want to access: ')
port = int(input('Enter the port you want to connect to: '))
s.connect((server_name, port))
key = s.recv(1024)
fernet = Fernet(key)
chat(s,fernet)
s.close()

