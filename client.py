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
        # self.name= name
        rcv = Thread(target=self.recieve)
        rcv.start()
        self.layout(name)


    def recieve(self):
        global client
        while(True):
            try:
                msg = client.recv(2048).decode("utf-8")
                if msg.lower() == "nickname":
                    client.send(self.name.encode("utf-8"))
                else:
                    self.show_msg(msg)
            except:
                print("An error occured!")
                client.close()
                break

    def on_closing(self):
        print("yes")
        global client
        client.close()
        self.window.destroy()
    def send(self, msg):
        self.textArea.config(state=DISABLED)
        self.msg = msg
        self.msgEntry.delete(0, END)
        snd = Thread(target=self.write)
        snd.start()
    def write(self):
        global client
        self.textArea.config(state=DISABLED)
        while(True):
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode("utf-8"))
            self.show_msg(message)
            break
    def show_msg(self, message):
        print(message)
        self.textArea.config(state=NORMAL)
        self.textArea.insert(END, message+"\n\n")
        self.textArea.config(state=DISABLED)
        self.textArea.see(END)
    def layout(self, name):
        self.name = name
        self.window.deiconify()
        self.window.title("Chat Room")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg="#17202A")

        self.nameLabel = Label(self.window, text=name, font="sans-serif 12", bg="#17202A", fg="cyan")
        self.nameLabel.place(relx=0.5, rely=0.05, anchor=CENTER)

        self.lineLabel = Label(self.window, width=450,  bg="cyan")
        self.lineLabel.place(relx=0, rely = 0.1, relheight=0.012)

        self.textArea = Text(self.window, width=20, height=2, bg="#17202A", fg="cyan", font="sans-serif 12", padx=5, pady=5)
        self.textArea.config(state=DISABLED)
        self.textArea.place(relwidth=1, rely=0.12, relheight=0.745)
        self.labelBottom = Label(self.window, bg="cyan", fg="black", font="sans-serif 14 bold", height=18)
        self.labelBottom.place(relwidth=1, rely=0.825)
        self.msgEntry = Entry(self.labelBottom, width=80, bg="#17202A", fg="cyan")
        self.msgEntry.place(relwidth=0.80, relheight=0.2, rely=0.008, relx=0.011)

        self.sendButton = Button(self.labelBottom, text="Send", font="sans-serif 14", command=lambda: self.send(self.msgEntry.get()))
        self.sendButton.place(relx=0.84, rely=0.035)

        self.scrollBar = Scrollbar(self.textArea)
        self.scrollBar.place(relheight=1, relx=0.974)
        self.scrollBar.config(command=self.textArea.yview)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

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
