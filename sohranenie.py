import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

def open_info(mess:str): 
    messagebox.showinfo(title="Информация", message=f"Файл в формате {mess} успешно сохранен!", default="ok")
def open_warning(mess:str): 
    messagebox.showwarning(title="Предупреждение", message=f"Предупреждение!\nСохранение файла в формате {mess} пока не реализованно!", default="ok")
def open_error(mess:str): 
    messagebox.showerror(title="Ошибка", message=f"Сообщение об ошибке?\n{mess}", default="ok")

class Window(tk.Tk):
    def __init__(self, dan:List):
        self.__dan = dan
        super().__init__()
        # конфигурация окна
        self.title("Выбор формата")
        self.geometry("250x200")
        listbox = ("txt", "Exel", "CVS", "JSON")
        listbox_var = tk.StringVar()
        self.frame_c= ttk.Frame(self)
        self.combobox = ttk.Combobox(self.frame_c, textvariable=listbox_var, values=listbox, state="readonly")
        self.combobox.current(0)
        self.combobox.grid(row=0, column=0, columnspan=2, sticky=tk.N)
        # определение кнопки
        self.button2 = ttk.Button(self.frame_c, text="Сохранить", command=lambda: self.pet(self.combobox.get())).grid(row=1, column=0, sticky=tk.N)
        self.button = ttk.Button(self.frame_c, text="Закрыть", command=self.button_clicked).grid(row=1, column=1, sticky=tk.N)
        self.frame_c.pack(anchor="center", expand=True)
        
    def button_clicked(self):
        self.destroy()
    
    def pet(self, listbox_v):
        if listbox_v == "txt":
            with open("otch.txt", "w", encoding="utf8") as file:
                for v in self.__dan:
                    for number in v:
                        file.write(str(number) + "\t")
                    file.write("\n")
            open_info(listbox_v)
        elif listbox_v == "Exel":
            open_warning(listbox_v)
        elif listbox_v == "CVS":
            with open("otch.cvs", "w", encoding="utf8") as file:
                for v in self.__dan:
                    for number in v:
                        file.write(str(number) + ";")
                    file.write("\n")
            open_info(listbox_v)
        elif listbox_v == "JSON":
            open_warning(listbox_v)
        else:
            open_error(f"#{listbox_v}")
