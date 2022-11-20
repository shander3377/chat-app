import socket
from threading import Thread
from tkinter import *

# nick = str(input("Enter your nickname: "))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_Address= "127.0.0.1"
port= 8000
client.connect((ip_Address, port))

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.login=Toplevel()
        self.login.title("Title")
        self.login.geometry("200x200")
        self.loginLabel = Label(self.login, text="Please Login", justify="center", font=("sans-serif", 14))
        self.loginLabel.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.nameLabel = Label(self.login, text="Name: ", font=("sans-serif", 10))
        self.nameLabel.place(relx=0.1, rely=0.4)
        self.nameEntry = Entry(self.login)
        self.nameEntry.place(relx=0.3, rely=0.4)
        self.loginButton = Button(self.login, text="Log In", bg="LightSkyBlue", font=("sans-serif", 14), command=lambda:self.goAhead(self.nameEntry.get()))
        self.loginButton.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.name= name
        rcv = Thread(target=self.recieve)
        rcv.start()

    def recieve(self):
        global client
        while(True):
            try:
                msg = client.recv(2048).decode("utf-8")
                if msg.lower() == "nickname":
                    client.send(self.name.encode("utf-8"))
                else:
                    pass
            except:
                print("An error occured")
                client.close()
                break;

GUI()       

# def write():
#     while(True):
#         msg = str(input())
#         client.send(msg.encode("utf-8"))

# while(True):
#     recieve_thread = Thread(target=recieve)
#     write_thread = Thread(target=write)
#     recieve_thread.start()
#     write_thread.start()
