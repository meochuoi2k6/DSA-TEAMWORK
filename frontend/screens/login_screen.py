# File: frontend/screens/login_screen.py
import json
import os
import logging
from PIL import Image
# Sửa lại import để tường minh hơn
from customtkinter import (CTkFrame, CTkLabel, CTkImage, CTkEntry, 
                           CTkCheckBox, CTkButton, END, LEFT, TOP, X, ANCHOR, CENTER)
from frontend.CTkMessagebox import CTkMessagebox
from .register_screen import RegisterScreen

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data store", "password.json")
MEMBER_PATH = os.path.join(BASE_DIR, "data store", "member.json")
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

class LoginPage(CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        #... (Toàn bộ nội dung còn lại của file này giữ nguyên như phiên bản hoàn chỉnh lần trước)
        self.on_login_success = on_login_success
        logger.info("Khởi động module Login")
        
        # --- Bắt đầu xây dựng giao diện ---
        logo_image = CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(75, 75))
        email_image = CTkImage(Image.open(os.path.join(image_path, "mail.png")), size=(35, 35))
        password_image = CTkImage(Image.open(os.path.join(image_path, "lock.png")), size=(35, 35))

        self.loginframe = CTkFrame(self, fg_color="#111", corner_radius=15)
        self.loginframe.place(relx=0.5, rely=0.5, anchor="center")

        CTkLabel(self.loginframe, text=" Login", image=logo_image, compound=LEFT, font=("monospace", 40, "bold")).pack(pady=20, side=TOP, anchor="w", padx=100)
        CTkLabel(self.loginframe, text="Welcome to Project Manager", font=("monospace", 25, "bold")).pack(pady=13)

        self.username_frame = CTkFrame(self.loginframe, fg_color="#333")
        self.username_frame.pack(pady=10, ipadx=10, ipady=2)
        CTkLabel(self.username_frame, text="", image=email_image).pack(side=LEFT, padx=10)
        self.usernameInput = CTkEntry(self.username_frame, placeholder_text="Username", font=("monospace", 20, "bold"), width=300, fg_color="transparent", border_width=0)
        self.usernameInput.pack(side=LEFT, ipady=15)

        self.password_frame = CTkFrame(self.loginframe, fg_color="#333")
        self.password_frame.pack(pady=5, ipadx=10, ipady=2)
        CTkLabel(self.password_frame, text="", image=password_image).pack(side=LEFT, padx=10)
        self.passwordInput = CTkEntry(self.password_frame, placeholder_text="Password", font=("monospace", 20, "bold"), width=300, fg_color="transparent", border_width=0, show="*")
        self.passwordInput.pack(side=LEFT, ipady=10)

        self.show_password_btn = CTkCheckBox(self, text=" Show Password", font=("Canberra", 16), command=self.show_password)
        self.show_password_btn.place(in_=self.loginframe, relx=0.5, rely=0.6, anchor="w", x=-150)

        self.loginBtn = CTkButton(self.loginframe, text="LOG IN", text_color="black", font=("monospace", 20, "bold"), fg_color="#1ED765", corner_radius=10, hover_color="#1DB954", command=self.login)
        self.loginBtn.pack(side=TOP, fill=X, padx=110, pady=(50, 10), ipady=5)

        register_frame = CTkFrame(self.loginframe, fg_color="transparent")
        register_frame.pack(pady=(10,20))
        CTkLabel(register_frame, text="Chưa có tài khoản?").pack(side=LEFT)
        register_button = CTkButton(register_frame, text="Đăng ký ngay", fg_color="transparent", text_color="#1ED765", width=30, command=self.open_register_screen)
        register_button.pack(side=LEFT)

    # File: frontend/screens/login_screen.py

# Trong lớp LoginPage:
    def open_register_screen(self):
        """Mở cửa sổ đăng ký."""
        if self.winfo_exists():
            # Truyền logger vào cho màn hình đăng ký
            RegisterScreen(self, logger=logging.getLogger(__name__))

    def check_credentials(self, username, password):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                users = json.load(f)
            for user in users:
                if user["username"] == username and user["password"] == password:
                    return user["id"]
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        return None

    def get_user_info(self, user_id):
        try:
            with open(MEMBER_PATH, "r", encoding="utf-8") as f:
                members = json.load(f)
            for member in members:
                if member["id"] == user_id:
                    return member
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        return None

    def show_password(self):
        self.passwordInput.configure(show="")
        self.show_password_btn.configure(command=self.hide_password)

    def hide_password(self):
        self.passwordInput.configure(show="*")
        self.show_password_btn.configure(command=self.show_password)

    def login(self):
        username = self.usernameInput.get()
        password = self.passwordInput.get()
        
        if not username or not password:
            CTkMessagebox(title="Error", message="Username hoặc Password không được để trống!", icon="cancel", wraplength=300)
            return

        user_id = self.check_credentials(username, password)
        if not user_id:
            logger.warning(f"Đăng nhập không thành công với username: '{username}'")
            self.passwordInput.delete(0, END)
            CTkMessagebox(title="Error", message="Sai username hoặc password.", icon="cancel")
        else:
            logger.info(f"Đăng nhập thành công với username: '{username}'")
            user_info = self.get_user_info(user_id)
            if user_info:
                self.on_login_success(user_info)
            else:
                logger.error(f"Không tìm thấy thông tin thành viên cho user_id: {user_id}")
                CTkMessagebox(title="Lỗi nghiêm trọng", message="Không tìm thấy dữ liệu người dùng tương ứng!", icon="cancel")