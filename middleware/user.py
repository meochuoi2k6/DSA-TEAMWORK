import tkinter as tk
from tkinter import messagebox, font
import json
import os
from middleware.log import log_setting
import ctypes


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID_PATH = os.path.join(BASE_DIR, "data store", "id.json")
MEMBER_PATH = os.path.join(BASE_DIR, "data store", "member.json")
PROJECT_PATH = os.path.join(BASE_DIR, "data store", "project.json")

logger = log_setting(__name__)

# Lấy giá trị ID từ file json, load tạo đối tượng
def load_json(filepath = MEMBER_PATH):
    if not os.path.exists(filepath):
        logger.warning(f"File {filepath} không tồn tại")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        members = json.load(f)
    for member in members:
        if member["id"] == id:
            name = member["name"]
            phone = member["phoneNumber"]
            is_admin = member.get("isAdmin", 0) == 1
            if is_admin:
                logger.info(f"Trả về Admin với ID {id}")
                return Admin(id, name, phone)
                
            else:
                logger.info(f"Trả về User với ID {id}")
                return User(id, name, phone)
                
    logger.error(f"Không tìm thấy thành viên với ID {id}")
    return None
class Function:
    def __init__(self):
        self.current_command = []
     


class User(Function):
    def __init__ (self, id, name, phone):
        self.id = id
        self.name = name
        self.phone = phone
        self.is_admin = False
    


class Admin (User):
    def __init__(self, admin_id, name, phone):
        super().__init__(admin_id, name, phone)
        self.is_admin = True
    #def display_existed_member (self, path = MEMBER_PATH):

    


    
        
