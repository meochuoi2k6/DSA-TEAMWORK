import customtkinter as ctk
from tkinter import messagebox
import json, os
from middleware.log import log_setting

logger = log_setting(__name__)

# Cấu hình theme cho customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_PATH = os.path.join(BASE_DIR, "data store", "project.json")
MEMBER_PATH = os.path.join(BASE_DIR, "data store", "member.json")

# Màu dark mode
DARK_BG = "#222831"
DARK_FRAME = "#393E46"
DARK_ENTRY = "#23272F"
DARK_TEXT = "#EEEEEE"
DARK_BUTTON = "#00ADB5"
DARK_BUTTON_TEXT = "#FFFFFF"
ERROR_TEXT = "#FF5555"

class MainScreen(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color=DARK_BG)
        self.master = master
        self.user_info = user
        username = user.get("name", "Người dùng")
        self.pack(fill="both", expand=True)

        self.master.configure(fg_color=DARK_BG)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, fg_color=DARK_FRAME, width=180)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text=f"👋 {username}", font=("Arial", 14),
                     text_color=DARK_TEXT).pack(pady=(20, 10))

        self._create_sidebar_button("Thông tin", self.selfInfo)
        self._create_sidebar_button("Danh sách project", self.show_projects_list)
        self._create_sidebar_button("Tạo project", self.create_project)

        ctk.CTkButton(self.sidebar, text="Thoát", command=self.master.quit,
                      fg_color=ERROR_TEXT, text_color=DARK_BUTTON_TEXT).pack(side="bottom", pady=10)

        # --- Content Area ---
        self.content = ctk.CTkFrame(self, fg_color=DARK_BG)
        self.content.pack(side="right", fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.content, text="Chào mừng đến hệ thống quản lý dự án",
                                        font=("Arial", 16), text_color=DARK_TEXT)
        self.title_label.pack(pady=20)

        self.display_area = ctk.CTkTextbox(self.content, wrap="word", fg_color=DARK_ENTRY,
                                           text_color=DARK_TEXT, width=800, height=500)
        self.display_area.pack(padx=20, pady=10, fill="both", expand=True)
        self.display_area.configure(state="disabled")

        logger.info("Đã vào màn hình chính")

    def _create_sidebar_button(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command,
                            fg_color=DARK_BUTTON, text_color=DARK_BUTTON_TEXT)
        btn.pack(pady=10, fill="x", padx=10)

    def clear_display(self):
        self.display_area.configure(state="normal")
        self.display_area.delete("1.0", "end")

    def selfInfo(self):
        self.clear_display()
        logger.info(f"Người dùng {self.user_info.get('name', 'Người dùng')} đang xem thông tin cá nhân")
        self.title_label.configure(text="Thông tin cá nhân")

        self.display_area.insert("end", "📄 THÔNG TIN CÁ NHÂN\n\n")
        for key, value in self.user_info.items():
            self.display_area.insert("end", f"{key}: {value}\n")

        self.display_area.configure(state="disabled")

    def show_projects_list(self, filepath=PROJECT_PATH):
        self.clear_display()
        logger.info(f"Người dùng {self.user_info.get('name', 'Người dùng')} đang xem danh sách dự án")
        self.title_label.configure(text="Danh sách các dự án")

        if not os.path.exists(filepath):
            messagebox.showerror("Lỗi", f"Không tìm thấy file {filepath}")
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                projects = json.load(f)
        except json.JSONDecodeError as e:
            messagebox.showerror("Lỗi JSON", f"Lỗi đọc file JSON:\n{e}")
            return

        if not projects:
            messagebox.showinfo("Thông báo", "Không có dự án nào.")
            return

        for project in projects:
            self.display_area.insert("end", f"📌 Tên: {project['name']}\n📝 Mô tả: {project['description']}\n")
            self.display_area.insert("end", "👥 Thành viên:\n")
            for member in project.get("member", []):
                self.display_area.insert("end", f"  - {member['id']}\n")
            self.display_area.insert("end", "\n")

        self.display_area.configure(state="disabled")

    def create_project(self):
        self.clear_display()
        logger.warning(f"Người dùng {self.user_info.get('name')} đang cố gắng tạo dự án mới")
        self.title_label.configure(text="Tạo dự án mới")
        messagebox.showerror("Lỗi", "Tính năng đang trong quá trình phát triển")


class AdminScreen(MainScreen):
    def __init__(self, master, username):
        super().__init__(master, username)