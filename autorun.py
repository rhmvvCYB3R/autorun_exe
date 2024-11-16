import tkinter
from tkinter import Tk, ttk, messagebox, filedialog
import customtkinter
import os
import winreg as reg

window = customtkinter.CTk()
window.title("AUTORUN PATCHER")
window.geometry("720x540")
window.resizable(False, False)
window.config(background="grey")

directories = ""

def path_btn():
    global directories
    messagebox.showinfo("INFO","ВЫБЕРИТЕ .EXE ФАЙЛЫ ЧТОБЫ ДОБАВИТЬ В АВТОЗАГРУЗКУ!\n НАЖМИТЕ НА ОК ЧТОБЫ ПРОДОЛЖИТЬ....")
    path = filedialog.askopenfilename(
        initialdir="C:/", title="SELECT FILE", filetypes=(("Executable files", "*.exe"), ("All files", "*.*")))
    
    if path:
        directories = path
        file_path.delete(0, tkinter.END)
        file_path.insert(0, directories)

def patch_btn():
    global directories
    autorun = autorun_var.get()
    
    if not directories:
        messagebox.showerror(title="Ошибка", message="Выберите EXE файл для автозапуска!")
        return
    
    if autorun == 1:
        try:
            add_to_autorun(directories)
            messagebox.showinfo(title="Успех", message="Файл успешно добавлен в автозапуск!")
        except Exception as e:
            messagebox.showerror(title="Ошибка", message=str(e))
    elif autorun == 2:
        try:
            remove_from_autorun(directories)
            messagebox.showinfo(title="Успех", message="Файл успешно удален из автозапуска!")
        except Exception as e:
            messagebox.showerror(title="Ошибка", message=str(e))

def add_to_autorun(file_path):
    key = reg.HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        reg_key = reg.OpenKey(key, reg_path, 0, reg.KEY_WRITE)
        reg.SetValueEx(reg_key, os.path.basename(file_path), 0, reg.REG_SZ, file_path)
        reg.CloseKey(reg_key)
    except Exception as e:
        raise Exception("Не удалось добавить в автозапуск: " + str(e))

def remove_from_autorun(file_path):
    key = reg.HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        reg_key = reg.OpenKey(key, reg_path, 0, reg.KEY_WRITE)
        reg.DeleteValue(reg_key, os.path.basename(file_path))
        reg.CloseKey(reg_key)
    except Exception as e:
        raise Exception("Не удалось удалить из автозапуска: " + str(e))

text_info = customtkinter.CTkLabel(window, text="\nПрограмма для добавления файлов в автозапуск \nи также для удаления", font=("Compact", 16), text_color="red", bg_color="grey")
text_info.place(x=20, y=0)

text_auth = customtkinter.CTkLabel(window, text="rhmvvCYB3R", font=("Compact", 12), text_color="blue", bg_color="grey")
text_auth.place(x=640, y=520)

autorun_var = tkinter.IntVar()

autorun = customtkinter.CTkRadioButton(window, text="Добавить в АВТОЗАПУСК", fg_color="GREEN", bg_color="GREY", value=1, variable=autorun_var)
autorun.place(x=20, y=170)

dell_autorun = customtkinter.CTkRadioButton(window, text="Убрать с АВТОЗАПУСКА", fg_color="RED", bg_color="GREY", value=2, variable=autorun_var)
dell_autorun.place(x=20, y=200)

file_path = customtkinter.CTkEntry(window, width=400, height=35, font=("Compact", 13), text_color="blue", bg_color="grey")
file_path.insert(0, directories)
file_path.place(x=20, y=110)

file_path_btn = customtkinter.CTkButton(window, text="ОБЗОР", fg_color="BLACK", command=path_btn, bg_color="grey")
file_path_btn.place(x=424, y=115)

file_patch_btn = customtkinter.CTkButton(window, text="СОХРАНИТЬ", fg_color="BLACK", bg_color="grey", command=patch_btn)
file_patch_btn.place(x=580, y=500)

window.mainloop()
