import tkinter as tk
from tkinter import messagebox
import json, os
from middleware.log import log_setting

logger = log_setting(__name__)

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

class MainScreen(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master, bg=DARK_BG)
        self.master = master
        self.user_info = user
        username = user.get("name", "Người dùng")
        self.pack(fill='both', expand=True)

        self.master.configure(bg=DARK_BG)

        # --- Sidebar ---
        self.sidebar = tk.Frame(self, bg=DARK_FRAME, width=180)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text=f"👋 {username}", font=("Arial", 14),
                 bg=DARK_FRAME, fg=DARK_TEXT).pack(pady=(20, 10))

        self._create_sidebar_button("Thông tin", self.selfInfo)
        self._create_sidebar_button("Danh sách project", self.show_projects_list)
        self._create_sidebar_button("Tạo project", self.create_project)

        tk.Button(self.sidebar, text="Thoát", command=self.master.quit,
                  bg=ERROR_TEXT, fg=DARK_BUTTON_TEXT).pack(side="bottom", pady=10)

        # --- Content Area ---
        self.content = tk.Frame(self, bg=DARK_BG)
        self.content.pack(side="right", fill="both", expand=True)

        self.title_label = tk.Label(self.content, text="Chào mừng đến hệ thống quản lý dự án",
                                    font=("Arial", 16), bg=DARK_BG, fg=DARK_TEXT)
        self.title_label.pack(pady=20)

        self.display_area = tk.Text(self.content, wrap="word", bg=DARK_ENTRY,
                                    fg=DARK_TEXT, insertbackground=DARK_TEXT,
                                    width=80, height=25)
        self.display_area.pack(padx=20, pady=10, fill="both", expand=True)
        self.display_area.config(state='disabled')

        logger.info("Đã vào màn hình chính")

    def _create_sidebar_button(self, text, command):
        """Tạo nút trong sidebar với style dark mode."""
        btn = tk.Button(self.sidebar, text=text, command=command,
                        bg=DARK_BUTTON, fg=DARK_BUTTON_TEXT, relief="flat",
                        activebackground=DARK_FRAME)
        btn.pack(pady=10, fill="x", padx=10)

    def clear_display(self):
        self.display_area.config(state='normal')
        self.display_area.delete("1.0", tk.END)

    def selfInfo(self):
        self.clear_display()
        logger.info(f"Người dùng {self.user_info.get('name', 'Người dùng')} đang xem thông tin cá nhân")
        self.title_label.config(text="Thông tin cá nhân")

        self.display_area.insert(tk.END, "📄 THÔNG TIN CÁ NHÂN\n\n")
        for key, value in self.user_info.items():
            self.display_area.insert(tk.END, f"{key}: {value}\n")

        self.display_area.config(state='disabled')

    def show_projects_list(self, filepath=PROJECT_PATH):
        self.clear_display()
        logger.info(f"Người dùng {self.user_info.get('name', 'Người dùng')} đang xem danh sách dự án")
        self.title_label.config(text="Danh sách các dự án")

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
            self.display_area.insert(tk.END, f"📌 Tên: {project['name']}\n📝 Mô tả: {project['description']}\n")
            self.display_area.insert(tk.END, "👥 Thành viên:\n")
            for member in project.get("member", []):
                self.display_area.insert(tk.END, f"  - {member['id']}\n")
            self.display_area.insert(tk.END, "\n")

        self.display_area.config(state='disabled')

    def create_project(self):
        self.clear_display()
        logger.warning(f"Người dùng {self.user_info.get('name')} đang cố gắng tạo dự án mới")
        self.title_label.config(text="Tạo dự án mới")
        messagebox.showerror("Lỗi", "Tính năng đang trong quá trình phát triển")


class adminScreen(MainScreen):
    def __init__(self, master, username):
        super().__init__(master, username)
