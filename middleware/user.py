import tkinter as tk
from tkinter import messagebox, font
import os
from middleware.log import log_setting
import ctypes
import datetime as dt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID_PATH = os.path.join(BASE_DIR, "data store", "id.json")
MEMBER_PATH = os.path.join(BASE_DIR, "data store", "member.json")
PROJECT_PATH = os.path.join(BASE_DIR, "data store", "project.json")

logger = log_setting(__name__)

# Lấy giá trị ID từ file json, load tạo đối tượng

class Function:
    def __init__(self):
        self.current_command = []
    #def createProject(self, name, description, members):
    def createProject(self, name, description, members, path):
        return


    


    


    
        
