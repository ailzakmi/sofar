# import json
import psutil
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from platform import uname

dan = []

def correct_size(bts, ending='iB'):
    size = 1024
    for item in ["", "K", "M", "G", "T", "P"]:
        if bts < size:
            return f"{bts:.2f}{item}{ending}"
        bts /= size

def creating_file():
    collect_info_dict = dict()
    if 'info' not in collect_info_dict:
        collect_info_dict['info'] = dict()
        collect_info_dict['info']['system_info'] = dict()
        collect_info_dict['info']['system_info'] = {'system': {'comp_name': uname().node,
                                                               'os_name': f"{uname().system} {uname().release}",
                                                               'version': uname().version,
                                                               'machine': uname().machine},
                                                    'processor': {'name': uname().processor,
                                                                  'phisycal_core': psutil.cpu_count(logical=False),
                                                                  'all_core': psutil.cpu_count(logical=True),
                                                                  'freq_max': f"{psutil.cpu_freq().max:.2f}Мгц"},
                                                    'ram': {'volume': correct_size(psutil.virtual_memory().total),
                                                            'aviable': correct_size(psutil.virtual_memory().available),
                                                            'used': correct_size(psutil.virtual_memory().used)}}

    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        if 'disk_info' not in collect_info_dict['info']:
            collect_info_dict['info']['disk_info'] = dict()
        if f"'device': {partition.device}" not in collect_info_dict['info']['disk_info']:
            collect_info_dict['info']['disk_info'][partition.device] = dict()
            collect_info_dict['info']['disk_info'][partition.device] = {'file_system': partition.fstype,
                                                                        'size_total': correct_size(
                                                                            partition_usage.total),
                                                                        'size_used': correct_size(
                                                                            partition_usage.used),
                                                                        'size_free': correct_size(
                                                                            partition_usage.free),
                                                                        'percent':
                                                                            f'{partition_usage.percent}'}

    for interface_name, interface_address in psutil.net_if_addrs().items():
        if interface_name == 'Loopback Pseudo-Interface 1':
            continue
        else:
            if 'net_info' not in collect_info_dict['info']:
                collect_info_dict['info']['net_info'] = dict()
            if interface_name not in collect_info_dict['info']['net_info']:
                collect_info_dict['info']['net_info'][interface_name] = dict()
                collect_info_dict['info']['net_info'][interface_name] = {
                    'mac': interface_address[0].address.replace("-", ":"),
                    'ipv4': interface_address[1].address,
                    'ipv6': interface_address[2].address}

    return collect_info_dict
'''''
def print_info(dict_info):
    for item in dict_info['info']:
        if item == "system_info":
            for elem in dict_info['info'][item]:
                if elem == 'system':
                    print(f"[+] Информация о системе\n"
                          f"\t- Имя компьютера: {dict_info['info'][item][elem]['comp_name']}\n"
                          f"\t- Опереционная система: {dict_info['info'][item][elem]['os_name']}\n"
                          f"\t- Сборка: {dict_info['info'][item][elem]['version']}\n"
                          f"\t- Архитектура: {dict_info['info'][item][elem]['machine']}\n")
                if elem == 'processor':
                    print(f"[+] Информация о процессоре\n"
                          f"\t- Семейство: {dict_info['info'][item][elem]['name']}\n"
                          f"\t- Физические ядра: {dict_info['info'][item][elem]['phisycal_core']}\n"
                          f"\t- Всего ядер: {dict_info['info'][item][elem]['all_core']}\n"
                          f"\t- Максимальная частота: {dict_info['info'][item][elem]['freq_max']}\n")
                if elem == 'ram':
                    print(f"[+] Оперативная память\n"
                          f"\t- Объем: {dict_info['info'][item][elem]['volume']}\n"
                          f"\t- Доступно: {dict_info['info'][item][elem]['aviable']}\n"
                          f"\t- Используется: {dict_info['info'][item][elem]['used']}\n")
        if item == "disk_info":
            for elem in dict_info['info'][item]:
                print(f"[+] Информация о дисках\n"
                      f"\t- Имя диска: {elem}\n"
                      f"\t- Файловая система: {dict_info['info'][item][elem]['file_system']}\n"
                      f"\t- Объем диска: {dict_info['info'][item][elem]['size_total']}\n"
                      f"\t- Занято: {dict_info['info'][item][elem]['size_used']}\n"
                      f"\t- Свободно: {dict_info['info'][item][elem]['size_free']}\n"
                      f"\t- Заполненность: {dict_info['info'][item][elem]['percent']}%\n")
        if item == "net_info":
            for elem in dict_info['info'][item]:
                print(f"[+] Информация о сети\n"
                      f"\t- Имя интерфейса: {elem}\n"
                      f"\t- MAC-адрес: {dict_info['info'][item][elem]['mac']}\n"
                      f"\t- IPv4: {dict_info['info'][item][elem]['ipv4']}\n"
                      f"\t- IPv6: {dict_info['info'][item][elem]['ipv6']}\n")

def main():
    if uname().system == "Windows":
        dict_info = creating_file()
        with open(f'info_{uname().node}.json', 'w', encoding='utf-8') as file:
            json.dump(dict_info, file, indent=4, ensure_ascii=False)
        print_info(dict_info)
    elif uname().system == "Linux":
        dict_info = creating_file()
        with open(f'info_{uname().node}.json', 'w', encoding='utf-8') as file:
            json.dump(dict_info, file, indent=4, ensure_ascii=False)
        print_info(dict_info)
'''''

def info_column():
    return (uname().node, f"{uname().system} {uname().release}", uname().version, uname().machine, uname().processor, psutil.cpu_count(logical=False),
         psutil.cpu_count(logical=True), f"{psutil.cpu_freq().max:.2f}Мгц", correct_size(psutil.virtual_memory().total), 
         correct_size(psutil.virtual_memory().available), correct_size(psutil.virtual_memory().used))

def info_no_local():
    return (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

class Window(Tk):
    def __init__(self):
        super().__init__()
        # конфигурация окна
        self.title("Новое окно")
        self.geometry("250x200")
        # определение кнопки
        self.button = ttk.Button(self, text="закрыть")
        self.button["command"] = self.button_clicked
        self.button.pack(anchor="center")
        self.button2 = ttk.Button(self, text="Печать")
        self.button2["command"] = self.pet
        self.button2.pack(anchor="center")
    def button_clicked(self):
        self.destroy()
    def pet(self):
        global dan
        for v, _ in dan:
            print(v)

def main():
    def zapol():
        ochistka()
        # person = ()
        if dofamin.get() == 1:
            person = info_column()
            tree.insert("", END, values=person)
            # person.clear()
        person = info_no_local()
        tree.insert("", END, values=person)
        # person.clear()
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
        l = [(tree.set(k, 0), k) for k in tree.get_children("")]
        for _,  (_, k) in enumerate(l):
            tree.delete(k)
    def sohranenie():
        global dan 
        dan = [(tree.set(k, 0), k) for k in tree.get_children("")]
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
    local_button = ttk.Checkbutton(frame, text="Показывать локальный компьютер", variable=dofamin).grid(row=1, column=0)
    frame.grid(row=0, column=0, sticky=EW)   
    # определяем данные для отображения
    people = [
        ("Tom", 38, "tom@email.com"), ("Bob", 42, "bob@email.com"), ("Sam", 28, "sam@email.com"),
        ("Alice", 33, "alice@email.com"), ("Kate", 21, "kate@email.com"), ("Ann", 24, "ann@email.com"),
        ("Mike", 34, "mike@email.com"), ("Alex", 52, "alex@email.com"), ("Jess", 28, "jess@email.com"),
        ]
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