import tkinter as tk
from tkinter import messagebox, font
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID_PATH = os.path.join(BASE_DIR, "data store", "id.json")
MEMBER_PATH = os.path.join(BASE_DIR, "data store", "member.json")


class User:
    def __init__ (self, id):
        self.id = id
    
    def is_admin (self, path = ID_PATH):
        if not os.path.exists(path):
            messagebox.showerror("Lỗi", f"Không tìm thấy file {path}")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                id_list = json.load(f)
        except json.JSONDecodeError as e:
            messagebox.showerror("Lỗi JSON", f"Lỗi đọc file JSON:\n{e}")
            return
        for id in id_list:
            if id_list[id] == 1:
                return True
        return False
    
class Admin (User):
    def __init__(self, admin_id):
        super().__init__(admin_id)
    #def display_existed_member (self, path = MEMBER_PATH):


    
        
