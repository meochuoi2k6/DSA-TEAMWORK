import tkinter as tk
from tkinter import messagebox
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_PATH = os.path.join(BASE_DIR, "data store", "project.json")
MEMBER_PATH = os.path.join(BASE_DIR, "data store", "member.json")


class MainScreen(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.pack()
        self.user_info = user
        username = user.get("name", "Người dùng")

        # Label chào mừng
        tk.Label(self, text=f"Chào mừng {username}", font=("Arial", 14)).place(x=30, y=10)

        # Các nút điều hướng
        tk.Button(self, text="Thông tin", command=self.selfInfo).pack()
        tk.Button(self, text="Danh sách project", command=self.show_projects_list).pack(pady=10)
        tk.Button(self, text="Tạo project", command=self.create_project).pack(pady=10)
        tk.Button(self, text="X", command=self.master.quit).place(x=650, y=10)

        # Khu hiển thị nội dung
        self.project_display = tk.Text(self, wrap="word", width=80, height=20)
        self.project_display.pack(padx=10, pady=10)
        self.project_display.config(state='disabled')

    def clear_display(self):
        self.project_display.config(state='normal')
        self.project_display.delete("1.0", tk.END)

    def selfInfo(self):
        self.clear_display()
        self.project_display.insert(tk.END, "THÔNG TIN CÁ NHÂN\n\n")
        for key, value in self.user_info.items():
            self.project_display.insert(tk.END, f"{key}: {value}\n")
        self.project_display.config(state='disabled')

    def show_projects_list(self, filepath=PROJECT_PATH):
        self.clear_display()

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
            self.project_display.insert(tk.END, f"Tên: {project['name']}\nMô tả: {project['description']}\n")
            self.project_display.insert(tk.END, "Thành viên:\n")
            for member in project.get("member", []):
                self.project_display.insert(tk.END, f"  - {member['id']}\n")
            self.project_display.insert(tk.END, "\n")

        self.project_display.config(state='disabled')

    def create_project(self):
        messagebox.showerror("Lỗi", "Tính năng đang trong quá trình phát triển")


class adminScreen(MainScreen):
    def __init__(self, master, username):
        super().__init__(master, username)