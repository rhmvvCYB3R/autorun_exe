import tkinter
from tkinter import Tk, messagebox, filedialog
import customtkinter
import os
import winreg as reg

window = customtkinter.CTk()
window.title("AUTORUN PATCHER")
window.geometry("720x540")
window.resizable(False, False)
window.config(background="#d6dbdf")

directories = ""



def delayed_frame():
    app = customtkinter.CTk()
    app.title("БАТ ФАЙЛ С ЗАДЕРЖКОЙ")
    app.geometry("720x540")
    app.resizable(False,False)
    app.config(background="#d6dbdf")


    app.mainloop()
    


def path_btn():
    global directories
    messagebox.showinfo("INFO", "ВЫБЕРИТЕ .EXE ФАЙЛЫ ЧТОБЫ ДОБАВИТЬ В АВТОЗАГРУЗКУ!\nНАЖМИТЕ НА ОК ЧТОБЫ ПРОДОЛЖИТЬ....")
    path = filedialog.askopenfilename(
        initialdir="C:/", title="SELECT FILE", filetypes=(("Executable files", "*.exe"), ("All files", "*.*"))
    )
    if path:
        directories = os.path.normpath(path) 
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
        program_name = os.path.splitext(os.path.basename(file_path))[0]
        normalized_path = os.path.normpath(file_path) 
        quoted_path = f'"{normalized_path}"'  
        reg.SetValueEx(reg_key, program_name, 0, reg.REG_SZ, quoted_path)
        reg.CloseKey(reg_key)
    except Exception as e:
        raise Exception("Не удалось добавить в автозапуск: " + str(e))


def remove_from_autorun(file_path):
    key = reg.HKEY_CURRENT_USER
    reg_path = "Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg_key = reg.OpenKey(key, reg_path, 0, reg.KEY_WRITE)
        program_name = os.path.splitext(os.path.basename(file_path))[0]
        reg.DeleteValue(reg_key, program_name)
        reg.CloseKey(reg_key)
    except FileNotFoundError:
        raise Exception("Файл не найден в автозагрузке!")
    except Exception as e:
        raise Exception("Не удалось удалить из автозапуска: " + str(e))

text_info = customtkinter.CTkLabel(
    window, text="\nПрограмма для добавления файлов в автозапуск \nи также для удаления",
    font=("Compact", 16), text_color="red", bg_color="#d6dbdf"
)
text_info.place(x=20, y=0)

text_auth = customtkinter.CTkLabel(window, text="rhmvvCYB3R", font=("Compact", 12), text_color="blue", bg_color="#d6dbdf")
text_auth.place(x=640, y=520)

autorun_var = tkinter.IntVar()

autorun = customtkinter.CTkRadioButton(
    window, text="Добавить в АВТОЗАПУСК", fg_color="GREEN", bg_color="#d6dbdf", value=1, variable=autorun_var,border_color="BLACK", text_color="GREEN",font=("Compact", 16)
)
autorun.place(x=20, y=170)

dell_autorun = customtkinter.CTkRadioButton(
    window, text="Убрать с АВТОЗАПУСКА", fg_color="RED", bg_color="#d6dbdf", value=2, variable=autorun_var,border_color="BLACK",text_color="Red",font=("Compact", 16)
)
dell_autorun.place(x=20, y=200)

file_path = customtkinter.CTkEntry(window, width=400, height=35, font=("Compact", 13), text_color="blue", bg_color="#d6dbdf")
file_path.insert(0, directories)
file_path.place(x=20, y=110)

file_path_btn = customtkinter.CTkButton(window, text="ОБЗОР", fg_color="BLACK", command=path_btn, bg_color="#d6dbdf")
file_path_btn.place(x=424, y=115)

file_patch_btn = customtkinter.CTkButton(window, text="СОХРАНИТЬ", fg_color="BLACK", bg_color="#d6dbdf", command=patch_btn)
file_patch_btn.place(x=580, y=500)

bat_crtn_btn = customtkinter.CTkButton(window, text="СОЗДАТЬ .BAT",fg_color="BLACK", bg_color="#d6dbdf", command=delayed_frame)
bat_crtn_btn.place(x=20,y=400)

def info_btn():
    messagebox.showinfo("Для чего это нужно?","Создайте бат файлы при условии того что если у вас при запуске системы вылетает приложение которую вы добавили в АВТОЗАПУСК.\nПосле создание .bat файла добавьте его в автозапуск")
bat_crt_info_btn = customtkinter.CTkButton(window,text="?",fg_color="red", bg_color="#d6dbdf", command=info_btn,width=40)
bat_crt_info_btn.place(x=163,y=400)

window.mainloop()