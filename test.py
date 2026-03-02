import socket
import psutil
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from platform import uname
from _thread import *

# global dofamin

def correct_size(bts, ending='iB'):
    size = 1024
    for item in ["", "K", "M", "G", "T", "P"]:
        if bts < size:
            return f"{bts:.2f}{item}{ending}"
        bts /= size
def info_column():
    return (uname().node, f"{uname().system} {uname().release}", uname().version, uname().machine, uname().processor, psutil.cpu_count(logical=False),
         psutil.cpu_count(logical=True), f"{psutil.cpu_freq().max:.2f}Мгц", correct_size(psutil.virtual_memory().total), 
         correct_size(psutil.virtual_memory().available), correct_size(psutil.virtual_memory().used))

def serv(it):
    def client_thread(message):
        # get_ident()
        # print(get_ident())
        while True:
            con, _ = client.accept()
            data = con.recv(1024)
            # print(data.decode())
            # print(message)
            if data.decode() == "OK":
                con.send(str(message).encode())
            # data = client.recv(1024)
            print("Sent: ", data.decode())
    # print(it)
    if not it:
        # exit_thread(mms)
        client.close()
        print("Server stop")
    client  = socket.socket()
    hostname = socket.gethostname()
    port = 12345
    client.bind((hostname, port))
    client.listen(2)
    message = ""
    for ms in info_column():
        message = message + str(ms) + ";"
    message = message[0:-1]
    # message = str(info_column())
    print("Server start")
    
    if it:
        start_new_thread(client_thread, (message, ))
        # print(mms)

def button_clicked(self):
    # _thread.exit_prog()
    self.destroy()

def main():
    window = Tk()
    window.title("Client")
    window.geometry('250x200')
    frame = ttk.Frame()
    button_n = ttk.Button(frame, text="Начать", command=lambda: serv(True)).grid(row=0, column=0, sticky=NSEW)
    # button_z = ttk.Button(frame, text="Закрыть", command=lambda: serv(False)).grid(row=0, column=1, sticky=NSEW)
    # button_n = ttk.Button(frame, text="Начать", command=start_new_thread(serv, (True, ))).grid(row=0, column=0, sticky=NSEW)
    button_z = ttk.Button(frame, text="Закрыть", command=lambda: button_clicked(window)).grid(row=0, column=1, sticky=NSEW)
    frame.pack(expand=1)
    window.mainloop()

if __name__ == "__main__":
    main()