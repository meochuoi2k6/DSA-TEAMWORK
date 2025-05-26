import tkinter as tk
from tkinter import messagebox, font
import json
import os
from middleware.log import log_setting

logger = log_setting(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data store", "password.json")
ID_PATH = os.path.join(BASE_DIR, "data store", "member.json")

#Setting cho logs:



class LoginScreen(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.pack(expand=True, fill='both')
        logger.info("Khởi động module Login")
        # Tạo font lớn
        large_font = font.Font(size=14)
        center_font = font.Font(size=25, weight='bold')
        # Frame con để chứa form login, căn giữa
        form_frame = tk.Frame(self)
        form_frame.place(relx=0.5, rely=0.5, anchor='center')  # Căn giữa cả chiều ngang lẫn dọc

        tk.Label(form_frame, text="Chào mừng đến với Quản Lý dự án", font =center_font).grid(row=0, column=0, columnspan=2, pady=20)
        # Username
        tk.Label(form_frame, text="Username:", font=large_font).grid(row=1, column=0, pady=10, padx=10, sticky='e')
        self.username_entry = tk.Entry(form_frame, font=large_font, width=25)
        self.username_entry.grid(row=1, column=1, pady=10, padx=10)

        # Password
        tk.Label(form_frame, text="Password:", font=large_font).grid(row=2, column=0, pady=10, padx=10, sticky='e')
        self.password_entry = tk.Entry(form_frame, show="*", font=large_font, width=25)
        self.password_entry.grid(row=2, column=1, pady=10, padx=10)

        # Login button
        login_button = tk.Button(form_frame, text="Login", font=large_font, command=self.login, width=20)
        login_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Error label
        self.error_label = tk.Label(form_frame, text="", font=large_font, fg="red")
        self.error_label.grid(row=4, column=0, columnspan=2)

    def check_credentials(self, username, password, filepath = DATA_PATH):
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            users = json.load(f)
        for user in users:
            if user["username"] == username and user["password"] == password:
                return user["id"]
        return None
    def get_info (self, user_id):
        filepath = os.path.join(BASE_DIR, "data store", "member.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            members = json.load(f)
        for member in members:
            if member["id"] == user_id:
                return member
        return None
            
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = self.check_credentials(username, password)
        if user_id:
            logger.info(f"Đăng nhập thành công '{username}'")
            self.error_label.config(text="")
            self.pack_forget()  
            name = self.get_info(user_id)
            self.on_login_success(name)
        else:
            logger.warning(f"Đăng nhập không thành công'{username}'")
            self.error_label.config(text="Invalid username or password.")
            self.after(2000, lambda: self.error_label.config(text=""))
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
