import psutil
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from platform import uname

import net
import sohranenie

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
"""
def info_no_local(col=11):
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
"""
def open_info(mess="Файл успешно сохранен!"): 
    showinfo(title="Информация", message=mess, default="ok")
def open_warning(mess="Сообщение о предупреждении"): 
    showwarning(title="Предупреждение", message=mess, default="ok")
def open_error(mess="Сообщение об ошибке"): 
    showerror(title="Ошибка", message=mess, default="ok")

def main():
    def zapol():
        ochistka()
        if dofamin.get() == 1:
            person = info_column()
            tree.insert("", END, values=person)
        # person = info_no_local()
        person = net.main()
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
    def sohranen():
        dan = []
        dan.append(list(tree['columns']))
        for row in tree.get_children(""):
            var = [(tree.set(row, k)) for k in range(len(tree['columns']))]
            dan.append(var)
        window = sohranenie.Window(dan)

    window = Tk()
    window.title("Разработка программного обеспечения для аудита аппаратной и программной конфигурации ПК")
    window.geometry('715x400')
    window.rowconfigure(index=1, weight=1)
    window.columnconfigure(index=0, weight=1)
    dofamin = IntVar()
    # position = {"padx":6, "pady":6, "anchor":NW}
    frame = ttk.Frame(borderwidth=1, relief=SOLID)
    button_1 = ttk.Button(frame, text="Получить сведения", command=zapol).grid(row=0, column=0)
    button_2 = ttk.Button(frame, text="Составить отчет", command=sohranen).grid(row=0, column=1)
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
