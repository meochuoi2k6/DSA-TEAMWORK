# File: middleware/module_project.py
import ctypes
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DLL_PATH = os.path.join(BASE_DIR, "cCode", "lib", "createProject.dll")

try:
    c_lib = ctypes.CDLL(DLL_PATH)
except OSError as e:
    print(f"LỖI: Không thể tải file DLL tại đường dẫn: {DLL_PATH}")
    raise e

# --- Định nghĩa các hàm C ---
c_create_project = c_lib.create_project
c_create_project.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int]
c_create_project.restype = None

c_delete_project = c_lib.delete_project_by_id
c_delete_project.argtypes = [ctypes.c_char_p]
c_delete_project.restype = None

c_add_task = c_lib.add_task_to_project
c_add_task.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
c_add_task.restype = None

c_get_next_id = c_lib.get_next_id
c_get_next_id.argtypes = [ctypes.c_char_p]
c_get_next_id.restype = ctypes.c_char_p

c_free_string = c_lib.free_c_string
c_free_string.argtypes = [ctypes.c_char_p]
c_free_string.restype = None

c_update_task_status = c_lib.update_task_status
c_update_task_status.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
c_update_task_status.restype = None


# --- Các hàm Python để Frontend gọi ---

def get_next_id(id_type: str) -> str:
    id_bytes = c_get_next_id(id_type.encode('utf-8'))
    try:
        py_string = id_bytes.decode('utf-8')
    finally:
        c_free_string(id_bytes)
    return py_string

def create_project(name, description, ownerID, startDate, endDate, status, memberID):
    c_name = name.encode('utf-8')
    c_description = description.encode('utf-8')
    c_ownerID = ownerID.encode('utf-8')
    c_startDate = startDate.encode('utf-8')
    c_endDate = endDate.encode('utf-8')
    currentMember = len(memberID)
    c_memberID_array = (ctypes.c_char_p * currentMember)()
    c_memberID_array[:] = [m.encode('utf-8') for m in memberID]
    c_create_project(c_name, c_description, c_ownerID, c_startDate, c_endDate, status, c_memberID_array, currentMember)
    print(f"Middleware: Đã gọi C để tạo dự án '{name}'")

def delete_project(project_id: str):
    c_project_id = project_id.encode('utf-8')
    c_delete_project(c_project_id)
    print(f"Middleware: Đã gọi C để xóa dự án '{project_id}'")

def add_task(project_id: str, title: str, description: str, assignee_id: str):
    c_project_id = project_id.encode('utf-8')
    c_title = title.encode('utf-8')
    c_description = description.encode('utf-8')
    c_assignee_id = assignee_id.encode('utf-8') if assignee_id else None
    c_add_task(c_project_id, c_title, c_description, c_assignee_id)
    print(f"Middleware: Đã gọi C để thêm task '{title}' vào dự án '{project_id}'")

def update_task_status(project_id: str, task_id: str, new_status: str):
    """Hàm Python gọi hàm C để cập nhật trạng thái task."""
    c_project_id = project_id.encode('utf-8')
    c_task_id = task_id.encode('utf-8')
    c_new_status = new_status.encode('utf-8')
    
    c_update_task_status(c_project_id, c_task_id, c_new_status)
    print(f"Middleware: Đã gọi C để cập nhật task '{task_id}' thành trạng thái '{new_status}'")