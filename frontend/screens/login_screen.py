import json
from customtkinter import *
from PIL import Image
from CTkMessagebox import CTkMessagebox
import time, threading

from middleware.log import log_setting
import logging
import os




logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data store", "password.json")
ID_PATH = os.path.join(BASE_DIR, "data store", "member.json")
image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "images")
class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.geometry("1000x600+200+40")
        self.root.configure(fg_color="#000")
        self.root.resizable(False, False)
        logger.info("Khởi động module Login")
        self.on_login_success = on_login_success
        Height = 12
        Width = 300
        icon_size = 35

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        spotify_image = CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(75, 75))
        email_image = CTkImage(Image.open(os.path.join(image_path, "mail.png")), size=(icon_size, icon_size))
        password_image = CTkImage(Image.open(os.path.join(image_path, "lock.png")), size=(icon_size, icon_size))

        self.loginframe = CTkFrame(self.root, fg_color="#111", corner_radius=15)

        CTkLabel(self.loginframe, text=" Login", image=spotify_image, compound=LEFT, font=("monospace", 40, "bold"), text_color="white").pack(pady=20, side=TOP, anchor="nw", padx=100)

        CTkLabel(self.loginframe, text="Welcome to Project manager", font=("monospace", 30, "bold"), text_color="white").pack(pady=13)

        self.username_frame = CTkFrame(self.loginframe, height=0, width=0, fg_color="#333")
        CTkLabel(self.username_frame, text="", image=email_image, fg_color="transparent", corner_radius=0).pack(side=LEFT, padx=10)
        self.usernameInput = CTkEntry(self.username_frame, placeholder_text="Email or username", font=("monospace", 20, "bold"), 
                                         height=Height, width=Width, text_color="#f3f3f3", fg_color="transparent", border_width=0)
        self.usernameInput.pack(side=LEFT, ipady=15)
        self.username_frame.pack(pady=10, ipadx=10, ipady=2)

        self.password_frame = CTkFrame(self.loginframe, height=0, width=0, fg_color="#333")
        CTkLabel(self.password_frame, text="", image=password_image, fg_color="transparent", corner_radius=0).pack(side=LEFT, padx=10)
        self.passwordInput = CTkEntry(self.password_frame, placeholder_text="Password", font=("monospace", 20, "bold"), 
                                         height=Height, width=Width, text_color="white", fg_color="transparent", border_width=0, show="*")
        self.passwordInput.pack(side=LEFT, ipady=10)
        self.password_frame.pack(pady=5, ipadx=10, ipady=2)

        self.show_password_btn = CTkCheckBox(self.loginframe, text=" Show Password", font=("Canbera", 21), command=self.show_password)
        self.show_password_btn.pack(pady=15, side=TOP, anchor="nw", padx=65)

        self.loginBtn = CTkButton(self.loginframe, text="LOG IN", text_color="black", font=("monospace", 20, "bold"), fg_color="white", corner_radius=10,
                                     hover_color="#dcdada", command=self.login)
        self.loginBtn.pack(side=TOP, fill=X, padx=55, pady=10, ipady=10)

        self.loginframe.pack(side=TOP, fill=BOTH, expand=True, pady=50, padx=260, ipady=10)

        progressbar_frame = CTkFrame(self.loginframe, height=0, width=0, fg_color="transparent")
        self.progressbar = CTkProgressBar(self.loginframe,  orientation="horizontal", mode="determinate", determinate_speed=1, 
                                             fg_color="white", height=5, progress_color="#1ED765", corner_radius=0, )
        self.progressbar.set(0)
        self.progressbar.pack(side=BOTTOM, fill=X)
        progressbar_frame.pack(side=BOTTOM, fill=X)

        self.thread = threading.Thread(target=self.loading)
    def check_credentials(self, username, password, filepath = DATA_PATH):
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            users = json.load(f)
        for user in users:
            if user["username"] == username and user["password"] == password:
                return user["id"]
    def show_password(self):
        self.passwordInput.configure(show="")
        self.show_password_btn.configure(command=self.hide_password)

    def hide_password(self):
        self.passwordInput.configure(show="*")
        self.show_password_btn.configure(command=self.show_password)

    def login(self):
        username = self.usernameInput.get()
        password = self.passwordInput.get()
        user_id = self.check_credentials(username, password)
        if len(username) == 0 or len(password) == 0:
            CTkMessagebox(title="Error", message=" Username or Password can't be empty ", icon="cancel", font=("monospace", 15, "bold"), text_color="white", wraplength=600)
        if not user_id:
            logger.warning(f"Đăng nhập không thành công'{username}'")
            self.usernameInput.delete(0, END)
            self.passwordInput.delete(0, END)
            CTkMessagebox(title="Error", message="Invalid username or password.", icon="cancel", font=("monospace", 15, "bold"), text_color="white", wraplength=600)
        else:
            logger.info(f"Đăng nhập thành công '{username}'")
            global user_name 
            user_name = self.get_info(user_id)
            self.progressbar.start()
            self.thread.start()
            
    def get_info (self, user_id): #Optimise to O(1)
        filepath = os.path.join(BASE_DIR, "data store", "member.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
             members = json.load(f)
        index = int(user_id)-1
        if members[index] != None:
            return members[index]
        return None
    def loading(self):
        time.sleep(1.1)
        self.progressbar.stop()
        self.progressbar.set(100)

        for widget in self.root.winfo_children():
            widget.destroy()
            self.on_login_success(user_name)
        

        # MainPage(self.root)

class MainPage:
    def __init__(self, master):
        self.root = master
        self.root.configure(fg_color="#222")
        self.root.resizable(True, True)
        CTkLabel(self.root, text=f"Welcome, {user_name}", font=("Canbera", 60), text_color="white").pack(fill=BOTH, pady=200)










# import tkinter as tk
# from tkinter import messagebox, font
# import json
# import os
# from middleware.log import log_setting
# import logging

# logger = logging.getLogger(__name__)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# DATA_PATH = os.path.join(BASE_DIR, "data store", "password.json")
# ID_PATH = os.path.join(BASE_DIR, "data store", "member.json")

# #DEFINE COLOR OF LOGGING SCREEN

# DARK_BG = "#222831"
# DARK_FRAME = "#393E46"
# DARK_ENTRY = "#23272F"
# DARK_TEXT = "#EEEEEE"
# DARK_BUTTON = "#00ADB5"
# DARK_BUTTON_TEXT = "#FFFFFF"
# ERROR_TEXT = "#FF5555"




# #Setting cho logs:


# class LoginScreen(tk.Frame):
#     def __init__(self, master, on_login_success):
#         super().__init__(master, bg = DARK_BG)
#         self.master = master
#         self.on_login_success = on_login_success
#         self.pack(expand=True, fill='both')
#         logger.info("Khởi động module Login")
#         # Tạo font lớn
#         large_font = font.Font(size=14)
#         center_font = font.Font(size=25, weight='bold')
#         # Frame con để chứa form login, căn giữa
#         form_frame = tk.Frame(self, bg = DARK_FRAME)
#         form_frame.place(relx=0.5, rely=0.5, anchor='center')  # Căn giữa cả chiều ngang lẫn dọc

#         tk.Label(form_frame, text="Chào mừng đến với Quản Lý dự án", font =center_font, bg = DARK_FRAME, fg = DARK_TEXT).grid(row=0, column=0, columnspan=2, pady=20)
#         # Username
#         tk.Label(form_frame, text="Username:", font=large_font, bg = DARK_FRAME, fg = DARK_TEXT).grid(row=1, column=0, pady=10, padx=10, sticky='e')
#         self.username_entry = tk.Entry(form_frame, font=large_font, width=25, bg=DARK_ENTRY, fg=DARK_TEXT, insertbackground=DARK_TEXT)
#         self.username_entry.grid(row=1, column=1, pady=10, padx=10)

#         # Password
#         tk.Label(form_frame, text="Password:", font=large_font, bg=DARK_FRAME, fg=DARK_TEXT).grid(row=2, column=0, pady=10, padx=10, sticky='e')
#         self.password_entry = tk.Entry(form_frame, show="*", font=large_font, width=25, bg=DARK_ENTRY, fg=DARK_TEXT, insertbackground=DARK_TEXT)
#         self.password_entry.grid(row=2, column=1, pady=10, padx=10)

#         # Login button
#         login_button = tk.Button(form_frame, text="Login", font=large_font, command=self.login, width=20, bg=DARK_BUTTON, fg=DARK_BUTTON_TEXT, activebackground=DARK_BUTTON, activeforeground=DARK_BUTTON_TEXT)
#         login_button.grid(row=3, column=0, columnspan=2, pady=20)

#         # Error label
#         self.error_label = tk.Label(form_frame, text="", font=large_font, fg="red", bg=DARK_FRAME)
#         self.error_label.grid(row=4, column=0, columnspan=2)

#     def check_credentials(self, username, password, filepath = DATA_PATH):
#         if not os.path.exists(filepath):
#             return None
#         with open(filepath, "r", encoding="utf-8") as f:
#             users = json.load(f)
#         for user in users:
#             if user["username"] == username and user["password"] == password:
#                 return user["id"]
#         return None
#     def get_info (self, user_id): #Optimise to O(1)
#         filepath = os.path.join(BASE_DIR, "data store", "member.json")
#         if not os.path.exists(filepath):
#             return None
#         with open(filepath, "r", encoding="utf-8") as f:
#             members = json.load(f)
#         index = int(user_id)-1
#         if members[index] != None:
#             return members[index]
#         return None
            
    # def login(self):
    #     username = self.username_entry.get()
    #     password = self.password_entry.get()
    #     user_id = self.check_credentials(username, password)
    #     if user_id:
    #         logger.info(f"Đăng nhập thành công '{username}'")
    #         self.error_label.config(text="")
    #         self.pack_forget()  
    #         name = self.get_info(user_id)
    #         self.on_login_success(name)
    #     else:
    #         logger.warning(f"Đăng nhập không thành công'{username}'")
    #         self.error_label.config(text="Invalid username or password.")
    #         self.after(2000, lambda: self.error_label.config(text=""))
    #         self.username_entry.delete(0, tk.END)
    #         self.password_entry.delete(0, tk.END)
# root = CTk(fg_color="black")
# root.title("Login Page")

# ...existing code...
# root.iconbitmap(os.path.join(image_path, "logo.ico"))

# LoginPage(root)

# root.mainloop()