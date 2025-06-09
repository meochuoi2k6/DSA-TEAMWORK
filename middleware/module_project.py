import datetime as dt
import ctypes
import os
from ctypes import POINTER

MAX_MEMBER = 10
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.join(BASE_DIR, "data store", "project.json")
createProject = ctypes.CDLL(os.path.join(BASE_DIR, "cCode", "lib", "createProject.dll"))


# Define Task structure
class Task(ctypes.Structure):
    pass

Task._fields_ = [
    ("taskID", ctypes.c_char * 11),
    ("projectID", ctypes.c_char * 10),
    ("title", ctypes.c_char * 100),
    ("description", ctypes.c_char * 200),
    ("assigneeID", ctypes.c_char * 8),
    ("dueDate", ctypes.c_char * 20),
    ("status", ctypes.c_int),
    ("next", ctypes.POINTER(Task)),
]

# Define Project structure
class Project(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * 50),
        ("projectID", ctypes.c_char * 11),
        ("ownerID", ctypes.c_char * 8),
        ("memberID", (ctypes.c_char * 8) * MAX_MEMBER),
        ("currentMember", ctypes.c_int),
        ("description", ctypes.c_char * 200),
        ("startDate", ctypes.c_char * 20),
        ("endDate", ctypes.c_char * 20),
        ("status", ctypes.c_int),
        ("members", ctypes.c_char * 1 * 10),  # Không sử dụng
        ("tasks", ctypes.POINTER(Task)),
    ]

    def __init__(self):
        super().__init__()
        self._py_name = ""
        self._py_description = ""
        self._py_members = []
        self._py_creator = ""
        self._py_project_id = b""
        self._py_start_date = dt.datetime.now().strftime("%Y-%m-%d")
        self._py_end_date = "Not completed"
        self.status = 0
        self.tasks = None

    def create_project(self, name, description, members, creator_id):
        self._py_name = name
        self._py_description = description
        self._py_members = members
        self._py_creator = creator_id
        self._py_project_id = createProject.get_next_project_id(name.encode("utf-8"))

    def set_status(self, status: int):
        if status < 0 or status > 3:
            raise ValueError("Invalid status code. Must be between 0 and 3.")
        self.status = status
        self._py_end_date = dt.datetime.now().strftime("%Y-%m-%d") if status == 2 else "Not completed"

    def save_project(self):
        # Gán dữ liệu vào struct C
        self.name = self._py_name.encode("utf-8")
        self.description = self._py_description.encode("utf-8")
        self.ownerID = self._py_creator.encode("utf-8")
        self.projectID = self._py_project_id
        self.startDate = self._py_start_date.encode("utf-8")
        self.endDate = (self._py_end_date.encode("utf-8")
                        if self._py_end_date != "Not completed" else b"Not completed")

        for i in range(MAX_MEMBER):
            self.memberID[i] = (self._py_members[i] if i < len(self._py_members) else b"")
        self.currentMember = len(self._py_members)

        createProject.save_project_to_json(ctypes.byref(self))


# Định nghĩa các hàm từ DLL
createProject.get_next_project_id.argtypes = [ctypes.c_char_p]
createProject.get_next_project_id.restype = ctypes.c_char_p

createProject.save_project_to_json.argtypes = [POINTER(Project)]
createProject.save_project_to_json.restype = None



# TEST dữ liệu
if __name__ == "__main__":
    # Tạo một task
    task = Task()
    task.taskID = b"0000000001"
    task.projectID = b"PJT00001"
    task.title = b"Task Title"
    task.description = b"Some description for the task"
    task.assigneeID = b"USR00001"
    task.dueDate = b"2025-07-01"
    task.status = 0
    task.next = None

    # Tạo một project
    project = Project()
    project.create_project("My Project", "A test project", [b"USR00001", b"USR00002"], "USR00001")
    project.tasks = ctypes.pointer(task)
    project.save_project()