import tkinter as tk
from tkinter import messagebox
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_PATH = os.path.join(BASE_DIR, "data store", "project.json")

class MainScreen(tk.Frame):
    def __init__ (self, master, username):
        super().__init__(master)
        self.master = master
        self.pack()

        welcome_msg = f"Welcome {username}"
        tk.Label(self, text=welcome_msg, font=("Arial", 14)).pack(pady=20)
        tk.Button(self, text="Thoát", command=self.master.quit).pack(pady=10)


        tk.Button(self, text="Project List", command=self.show_projects_list).pack(pady=10)
        tk.Button(self, text="Create a project", command=self.create_project).pack(pady=10)
    def show_projects_list(self, filepath=DATA_PATH):
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

        project_list = ""
        for project in projects:
            project_list += f"Tên: {project['name']}\nMô tả: {project['description']}\n"
            project_list += "Thành viên:\n"
            for member in project.get("member", []):
                project_list += f"  - {member['name']} ({member['id']}): {member['role']}\n"
            project_list += "\n"

        messagebox.showinfo("Danh sách dự án", project_list)
