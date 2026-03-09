import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

def open_info(mess="Файл успешно сохранен!"): 
    messagebox.showinfo(title="Информация", message=mess, default="ok")

class Window(tk.Tk):
    def __init__(self, dan:List):
        self.__dan = dan
        super().__init__()
        # конфигурация окна
        self.title("Выбор формата")
        self.geometry("250x200")
        listbox = ("txt", "Exel", "CVS", "JSON")
        listbox_var = tk.StringVar()
        # print(listbox_var.get())
        self.frame_c= ttk.Frame(self)
        self.combobox = ttk.Combobox(self.frame_c, textvariable=listbox_var, values=listbox, state="readonly")
        self.combobox.current(0)
        self.combobox.grid(row=0, column=0, columnspan=2, sticky=tk.N)
        # self.label = ttk.Label(self.frame_c, textvariable=listbox_var).pack(anchor="center")
        # определение кнопки
        self.button2 = ttk.Button(self.frame_c, text="Сохранить", command=lambda: self.pet(self.combobox.get())).grid(row=1, column=0, sticky=tk.N)
        self.button = ttk.Button(self.frame_c, text="Закрыть", command=self.button_clicked).grid(row=1, column=1, sticky=tk.N)
        self.frame_c.pack(anchor="center", expand=True)
        
    def button_clicked(self):
        self.destroy()
    
    def pet(self, listbox_v):
        if listbox_v == "txt":
            print(listbox_v)
            with open("otch.txt", "w", encoding="utf8") as file:
                for v in self.__dan:
                    for number in v:
                        file.write(str(number) + "\t")
                    file.write("\n")
            open_info()
        elif listbox_v == "Exel":
            print(listbox_v)
        elif listbox_v == "CVS":
            print(listbox_v)
        elif listbox_v == "JSON":
            print(listbox_v)
        else:
            print(f"#{listbox_v}")
