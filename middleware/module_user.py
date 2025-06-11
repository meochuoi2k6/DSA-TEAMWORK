# File: middleware/module_user.py
import json
import os
import uuid
# from middleware.module_project import get_next_id
from middleware.log import log_setting  # Import hàm log

# Tạo một logger riêng cho module này
logger = log_setting(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSWORD_FILE = os.path.join(BASE_DIR, "data store", "password.json")
MEMBER_FILE = os.path.join(BASE_DIR, "data store", "member.json")

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def register_user(username, password, full_name):
    """Hàm xử lý logic đăng ký người dùng mới với logging chi tiết."""
    logger.debug(f"Bắt đầu quy trình đăng ký cho username: '{username}'")

    # 1. Kiểm tra username đã tồn tại chưa
    passwords_data = load_json(PASSWORD_FILE)
    for user in passwords_data:
        if user.get('username') == username:
            logger.warning(f"Thất bại: Tên người dùng '{username}' đã tồn tại.")
            return (False, f"Tên người dùng '{username}' đã tồn tại.")

    # 2. Sinh ID người dùng mới bằng Python (UUID4) thay vì gọi C để tránh crash
    new_user_id = str(uuid.uuid4())
    logger.info(f"Sinh ID người dùng mới bằng Python: {new_user_id}")

    # 3. Tạo thông tin người dùng mới
    new_password_entry = { "id": new_user_id, "username": username, "password": password }
    new_member_entry = { "id": new_user_id, "name": full_name, "role": 0 }

    # 4. Thêm vào dữ liệu và lưu lại file
    try:
        logger.debug("Chuẩn bị ghi vào file password.json...")
        passwords_data.append(new_password_entry)
        save_json(PASSWORD_FILE, passwords_data)
        logger.debug("Ghi password.json thành công.")

        logger.debug("Chuẩn bị ghi vào file member.json...")
        members_data = load_json(MEMBER_FILE)
        members_data.append(new_member_entry)
        save_json(MEMBER_FILE, members_data)
        logger.debug("Ghi member.json thành công.")
    except IOError as e:
        logger.error(f"Lỗi I/O khi ghi file JSON: {e}", exc_info=True)
        return (False, "Lỗi khi lưu dữ liệu người dùng.")
    except Exception as e:
        logger.error(f"Lỗi không xác định khi ghi file: {e}", exc_info=True)
        return (False, "Lỗi không xác định khi lưu dữ liệu.")

    logger.info(f"Hoàn tất đăng ký cho user ID: {new_user_id}")
    return (True, "Tạo tài khoản thành công!")
