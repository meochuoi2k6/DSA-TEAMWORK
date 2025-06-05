from middleware.user import Function
from middleware.module_project import Project
import json
import os
from middleware.log import log_setting
import datetime as dt

logger = log_setting(__name__)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID_PATH = os.path.join(BASE_DIR, "data store", "id.json")
MEMBER_PATH = os.path.join(BASE_DIR, "data store", "member.json")
PROJECT_PATH = os.path.join(BASE_DIR, "data store", "project.json")

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
    #Khi load file JSON sẽ trả về User, hoặc Admin nếu thấy id, None nếu không thấy ID
    logger.error(f"Không tìm thấy thành viên với ID {id}")
    return None

class User(Function):
    def get_projects(self, path = PROJECT_PATH):
        if not os.path.exists(path):
            logger.warning(f"File {path} không tồn tại")
            return []
        with open(path, "r", enconding = "utf-8") as f:
            projects = json.load(f)
        user_projects = []
        for project in projects:
            if self.id in project["memberID"]:
                user_projects.append(Project(**project))
        logger.info(f"Đã trả về {len(user_projects)} cho người dùng {self.name}")
        return user_projects
    def __init__ (self, id, name, phone):

        self.id = id
        self.name = name
        self.phone = phone
        self.is_admin = False
        self.project = self.get_projects(path = PROJECT_PATH)
    #Trả về một mảng project cho đối tượng

        
        
class Admin (User):
    def __init__(self, admin_id, name, phone):
        super().__init__(admin_id, name, phone)
        self.is_admin = True
    #def display_existed_member (self, path = MEMBER_PATH):