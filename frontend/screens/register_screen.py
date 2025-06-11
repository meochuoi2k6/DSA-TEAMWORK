# File: frontend/screens/register_screen.py
import customtkinter as ctk
from frontend.CTkMessagebox import CTkMessagebox
from middleware import module_user
import logging

class RegisterScreen(ctk.CTkToplevel):
    def __init__(self, master, logger): # Nhận logger từ màn hình cha
        super().__init__(master)
        self.logger = logger
        self.title("Tạo Tài Khoản Mới")
        self.geometry("400x500")
        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(self, text="Đăng Ký Tài Khoản", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Full Name, Username, Password, Confirm Password entries (giữ nguyên)
        # ... (code các widget không đổi)
        ctk.CTkLabel(self, text="Tên đầy đủ:").pack(padx=20, anchor="w")
        self.full_name_entry = ctk.CTkEntry(self, width=360)
        self.full_name_entry.pack(padx=20, pady=5, fill="x")
        ctk.CTkLabel(self, text="Tên đăng nhập:").pack(padx=20, anchor="w")
        self.username_entry = ctk.CTkEntry(self, width=360)
        self.username_entry.pack(padx=20, pady=5, fill="x")
        ctk.CTkLabel(self, text="Mật khẩu:").pack(padx=20, anchor="w")
        self.password_entry = ctk.CTkEntry(self, width=360, show="*")
        self.password_entry.pack(padx=20, pady=5, fill="x")
        ctk.CTkLabel(self, text="Xác nhận mật khẩu:").pack(padx=20, anchor="w")
        self.confirm_password_entry = ctk.CTkEntry(self, width=360, show="*")
        self.confirm_password_entry.pack(padx=20, pady=5, fill="x")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30)
        register_button = ctk.CTkButton(button_frame, text="Đăng Ký", command=self.submit_registration)
        register_button.pack(side="left", padx=10)
        cancel_button = ctk.CTkButton(button_frame, text="Hủy", fg_color="gray", command=self.destroy)
        cancel_button.pack(side="left", padx=10)

    def submit_registration(self):
        full_name = self.full_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not all([full_name, username, password, confirm_password]):
            CTkMessagebox(master=self, title="Lỗi", message="Vui lòng điền đầy đủ thông tin.", icon="cancel")
            return
        if password != confirm_password:
            CTkMessagebox(master=self, title="Lỗi", message="Mật khẩu xác nhận không khớp.", icon="cancel")
            return

        self.logger.info(f"Bắt đầu gọi middleware để đăng ký user: {username}")
        success, message = module_user.register_user(username, password, full_name)
        self.logger.info(f"Kết quả từ middleware: success={success}, message='{message}'")

        if success:
            self.logger.debug("Chuẩn bị hiển thị messagebox thành công.")
            CTkMessagebox(master=self, title="Thành công", message=message, icon="check")
            self.logger.debug("Đã hiển thị messagebox. Chuẩn bị hủy cửa sổ đăng ký.")
            self.destroy()
            self.logger.debug("Đã hủy cửa sổ đăng ký thành công.")
        else:
            CTkMessagebox(master=self, title="Lỗi", message=message, icon="cancel")