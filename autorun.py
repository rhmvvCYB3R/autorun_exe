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


name_file = ""
delay_time = ""
path = ""


def delayed_frame():
    app = customtkinter.CTk()
    app.title("БАТ ФАЙЛ С ЗАДЕРЖКОЙ")
    app.geometry("720x540")
    app.resizable(False,False)
    app.config(background="#d6dbdf")

    text_info2 = customtkinter.CTkLabel(app,text="""
  
     ──▒▒▒▒▒────▒▒▒▒▒────▒▒▒▒▒────▄████▄
   ─▒▄─▒▄─▒──▒▄─▒▄─▒──▒▄─▒▄─▒──███▄█▀
─▒▒▒▒▒▒▒──▒▒▒▒▒▒▒──▒▒▒▒▒▒▒─▐████
  ─▒▒▒▒▒▒▒──▒▒▒▒▒▒▒──▒▒▒▒▒▒▒──█████▄
    ─▒─▒─▒─▒──▒─▒─▒─▒──▒─▒─▒─▒───▀████▀
    """,text_color="purple",bg_color="#d6dbdf")
    text_info2.place(x=100,y=430)

    
    def funk_find():
        global path
        messagebox.showinfo("INFO", "ВЫБЕРИТЕ .EXE ФАЙЛ ДЛЯ КОТОРОГО ХОТИТЕ СОЗДАТЬ .БАТ\nНАЖМИТЕ НА ОК ЧТОБЫ ПРОДОЛЖИТЬ....")
        path = filedialog.askopenfilename(
            initialdir="C:/", title="SELECT FILE", filetypes=(("Executable files", "*.exe"), ("All files", "*.*"))
        )
        if path:
            path = os.path.normpath(path)
            file_dir.delete(0, tkinter.END)
            file_dir.insert(0, path)

    def funk_creater():
        if path and delay_time:
            path_without_exe = os.path.dirname(path)
            name_file = os.path.basename(path)

            bat_data = f"""
@echo off
cd /d "{path_without_exe}"
timeout /t {delay_time}
start "" "{name_file}" 2>> error_log.txt
            """
            save_path = filedialog.asksaveasfilename(defaultextension=".bat", filetypes=[("Batch Files", "*.bat")])
            if save_path:
                with open(save_path, "w") as bat_file:
                    bat_file.write(bat_data)
                messagebox.showinfo("INFO", "Файл .BAT успешно создан!")
            else:
                messagebox.showerror("ERROR", "Не удалось сохранить .BAT файл.")
        else:
            messagebox.showerror("ERROR", "Не выбрано .EXE приложение или задержка.")

    text_info3 = customtkinter.CTkLabel(app, text="СОЗДАНИЕ .БАТ ФАЙЛА С ЗАДЕРЖКОЙ ЗАПУСКА!", text_color="red", bg_color="#d6dbdf", font=("COMPACT", 20))
    text_info3.place(x=95, y=10)

    file_dir = customtkinter.CTkEntry(app, width=400, height=35, font=("Compact", 13), text_color="blue", bg_color="#d6dbdf")
    file_dir.insert(0, path)
    file_dir.place(x=40, y=100)

    file_find_btn = customtkinter.CTkButton(app, text="ОБЗОР", fg_color="BLACK", command=funk_find, bg_color="#d6dbdf", width=80, height=30)
    file_find_btn.place(x=450, y=103)

    bat_creater_btn = customtkinter.CTkButton(app, text="СОЗДАТЬ ФАЙЛ!", command=funk_creater, bg_color="#d6dbdf", text_color="BLACK")
    bat_creater_btn.place(x=500, y=400)

    def combobox_callback(choice):
        global delay_time
        delay_time = choice

    combobox_var = customtkinter.StringVar(value="ВЫБЕРИТЕ ЗАДЕРЖУ(секунды)")  
    combobox = customtkinter.CTkComboBox(app, values=["ВЫБЕРИТЕ ЗАДЕРЖУ(секунды)","2", "3", "5", "8", "10"],
                                         command=combobox_callback, variable=combobox_var, width=250, fg_color="red", bg_color="#d6dbdf")
    combobox.set("ВЫБЕРИТЕ ЗАДЕРЖУ(секунды)")
    combobox.place(x=40, y=140)

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