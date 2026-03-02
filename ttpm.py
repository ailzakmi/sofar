import socket
import psutil
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import *
from platform import uname

dan = []

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

def info_no_local(col):
    server  =  socket.socket()
    hostname  = socket.gethostname()
    port = 12345
    server.connect((hostname, port))
    # server.listen(5)
    print("Server start")
    # con, _ = server.accept() #Принимаем клиента
    print("connection: ", server)
    message = "OK"
    server.send(message.encode())
    data = server.recv(1024)
    # con.close()
    message = (data.decode())
    # data = []
    data = list(message.split(";"))
    # for ms in message.split(";"):
    #     data.append(ms)
    print("Server ends")
    server.close()
    message = []
    message.append(data)
    return message
    # temp = []
    # for i in range(1,col+1):
    #     temp.append((i,i,i))

def open_info(mess="Файл успешно сохранен!"): 
    showinfo(title="Информация", message=mess, default="ok")
def open_warning(mess="Сообщение о предупреждении"): 
    showwarning(title="Предупреждение", message=mess, default="ok")
def open_error(mess="Сообщение об ошибке"): 
    showerror(title="Ошибка", message=mess, default="ok")
class Window(Tk):
    def __init__(self):
        super().__init__()
        # конфигурация окна
        self.title("Выбор формата")
        self.geometry("250x200")
        listbox = ("txt", "Exel", "CVS", "JSON")
        listbox_var = StringVar()
        # print(listbox_var.get())
        self.frame_c= ttk.Frame(self)
        self.combobox = ttk.Combobox(self.frame_c, textvariable=listbox_var, values=listbox, state="readonly")
        self.combobox.current(0)
        self.combobox.grid(row=0, column=0, columnspan=2, sticky=N)
        # self.label = ttk.Label(self.frame_c, textvariable=listbox_var).pack(anchor="center")
        # определение кнопки
        self.button2 = ttk.Button(self.frame_c, text="Печать", command=lambda: self.pet(listbox, self.combobox.get())).grid(row=1, column=0, sticky=N)
        self.button = ttk.Button(self.frame_c, text="закрыть", command=self.button_clicked).grid(row=1, column=1, sticky=N)
        self.frame_c.pack(anchor="center", expand=True)
        
    def button_clicked(self):
        self.destroy()
    
    def pet(self, listbox, listbox_v):
        global dan
        if (dan[0] == []):
            print("Пусто")
        match listbox_v.split():
            case ["txt"]:
                print(listbox_v)
                with open("otch.txt", "w", encoding="utf8") as file:
                    for v in dan:
                        for number in v:
                            file.write(str(number) + "\t")
                        file.write("\n")
                open_info()
            case ["Exel"]:
                print(listbox_v)
            case ["CVS"]:
                print(listbox_v)
            case ["JSON"]:
                print(listbox_v)
            case _:
                print(f"#{listbox_v}")

def main():
    def zapol():
        ochistka()
        # person = ()
        if dofamin.get() == 1:
            person = info_column()
            tree.insert("", END, values=person)
        person = info_no_local(len(tree['columns']))
        print(person)
        for k in person:
            tree.insert("", END, values=k)
    def sort(col, reverse):
        # получаем все значения столбцов в виде отдельного списка
        l = [(tree.set(k, col), k) for k in tree.get_children("")]
        # сортируем список
        l.sort(reverse=reverse)
        # переупорядочиваем значения в отсортированном порядке
        for index,  (_, k) in enumerate(l):
            tree.move(k, "", index)
        # в следующий раз выполняем сортировку в обратном порядке
        tree.heading(col, command=lambda: sort(col, not reverse))
    def ochistka():
        for k in tree.get_children(""):
            tree.delete(k)
    def sohranenie():
        global dan
        var = []
        dan.append(list(tree['columns']))
        for row in tree.get_children(""):
            var = [(tree.set(row, k)) for k in range(len(tree['columns']))]
            dan.append(var)
        # print(dan)
        window = Window()

    window = Tk()
    window.title("Разработка программного обеспечения для аудита аппаратной и программной конфигурации ПК")
    window.geometry('715x400')
    window.rowconfigure(index=1, weight=1)
    window.columnconfigure(index=0, weight=1)
    dofamin = IntVar()
    # position = {"padx":6, "pady":6, "anchor":NW}
    frame = ttk.Frame(borderwidth=1, relief=SOLID)
    button_1 = ttk.Button(frame, text="Получить сведения", command=zapol).grid(row=0, column=0)
    button_2 = ttk.Button(frame, text="Составить отчет", command=sohranenie).grid(row=0, column=1)
    local_button = ttk.Checkbutton(frame, text="Показывать локальный компьютер", variable=dofamin).grid(row=1, column=0, columnspan=2)
    frame.grid(row=0, column=0, sticky=EW)
    # определяем столбцы
    columns = ("comp_name", "os_name", "version", "machine", "processor_name", "processor_phisycal_core", "processor_all_core", 
               "processor_freq_max","raw_volume", "raw_aviable", "raw_used")

    frame_m = ttk.Frame(borderwidth=1, relief=SOLID)
    frame_m.rowconfigure(index=0, weight=1)
    frame_m.columnconfigure(index=0, weight=1)

    tree = ttk.Treeview(frame_m,columns=columns, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")
    # определяем заголовки
    for head in columns:
        tree.heading(head, text=f"{head}", anchor=W, command=lambda: sort(0, False))
    # tree.heading("age", text="Возраст", anchor=W)
    # добавляем данные
    for head, v in enumerate(columns, start=1):
        tree.column(f"#{head}", stretch=NO, width=len(v)*10)
    
    # добавляем горизонтальную прокрутку
    scrollbar = ttk.Scrollbar(frame_m,orient=HORIZONTAL, command=tree.xview)
    tree.configure(xscroll=scrollbar.set)
    scrollbar.grid(row=1, column=0, sticky="ew")
    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(frame_m,orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    frame_m.grid(row=1, column=0, sticky="nsew")
    window.mainloop()

if __name__ == "__main__":
    main()