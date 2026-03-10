import psutil
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror
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
            tree.insert("", tk.END, values=person)
        person = net.main()
        if person == []:
            open_error("Не найдены компьютеры в текущей сети!")
        else:
            for k in person:
                tree.insert("", tk.END, values=k)
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

    window = tk.Tk()
    window.title("Разработка программного обеспечения для аудита аппаратной и программной конфигурации ПК")
    window.geometry('715x400')
    window.rowconfigure(index=1, weight=1)
    window.columnconfigure(index=0, weight=1)
    dofamin = tk.IntVar()
    frame = ttk.Frame(borderwidth=1, relief=tk.SOLID)
    button_1 = ttk.Button(frame, text="Получить сведения", command=zapol).grid(row=0, column=0)
    button_2 = ttk.Button(frame, text="Составить отчет", command=sohranen).grid(row=0, column=1)
    local_button = ttk.Checkbutton(frame, text="Показывать локальный компьютер", variable=dofamin).grid(row=1, column=0, columnspan=2)
    frame.grid(row=0, column=0, sticky=tk.EW)
    # определяем столбцы
    columns = ("comp_name", "os_name", "version", "machine", "processor_name", "processor_phisycal_core", "processor_all_core", 
               "processor_freq_max","raw_volume", "raw_aviable", "raw_used")

    frame_m = ttk.Frame(borderwidth=1, relief=tk.SOLID)
    frame_m.rowconfigure(index=0, weight=1)
    frame_m.columnconfigure(index=0, weight=1)

    tree = ttk.Treeview(frame_m,columns=columns, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")
    # определяем заголовки
    for head in columns:
        tree.heading(head, text=f"{head}", anchor=tk.W, command=lambda: sort(0, False))
    # добавляем данные
    for head, v in enumerate(columns, start=1):
        tree.column(f"#{head}", stretch=tk.NO, width=len(v)*10)
    
    # добавляем горизонтальную прокрутку
    scrollbarx = ttk.Scrollbar(frame_m,orient=tk.HORIZONTAL, command=tree.xview)
    tree["xscrollcommand"]=scrollbarx.set
    scrollbarx.grid(row=1, column=0, sticky="ew")
    # добавляем вертикальную прокрутку
    scrollbary = ttk.Scrollbar(frame_m,orient=tk.VERTICAL, command=tree.yview)
    tree["yscrollcommand"]=scrollbary.set
    scrollbary.grid(row=0, column=1, sticky="ns")

    frame_m.grid(row=1, column=0, sticky="nsew")
    window.mainloop()

if __name__ == "__main__":
    main()
