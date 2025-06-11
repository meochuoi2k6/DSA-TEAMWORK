# File: run.py

import customtkinter as ctk
from frontend.screens.login_screen import LoginPage
from frontend.screens.main_screen import MainScreen, AdminScreen
from frontend.screens.project_detail_screen import ProjectDetailScreen
from middleware.log import log_setting
import json

class App(ctk.CTk):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.title("Project Management Tool")
        self.geometry("1100x720")
        self.current_screen = None
        self.show_login_screen()

    def show_login_screen(self):
        """Hiển thị màn hình đăng nhập."""
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = LoginPage(self, on_login_success=self.show_main_menu)
        # Hiển thị màn hình lên cửa sổ
        self.current_screen.pack(fill="both", expand=True)

    def is_admin(self, user_info, filepath="data store/member.json"):
        """Kiểm tra vai trò của người dùng."""
        user_id = user_info.get("id")
        if not user_id:
            return False
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                users = json.load(f)
            for user in users:
                if user["id"] == user_id:
                    return user.get("role") == 1
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        return False

    def show_main_menu(self, user_info):
        """Hiển thị màn hình chính sau khi đăng nhập thành công."""
        if self.current_screen:
            self.current_screen.destroy()
        
        if self.is_admin(user_info):
            self.current_screen = AdminScreen(self, user_info=user_info, logger=self.logger)
        else:
            self.current_screen = MainScreen(self, user_info=user_info, logger=self.logger)
        
        # === THÊM DÒNG CÒN THIẾU TẠI ĐÂY ===
        # Hiển thị màn hình lên cửa sổ
        self.current_screen.pack(fill="both", expand=True)
        
    def show_project_detail_screen(self, user_info, project_id):
        """Hiển thị màn hình chi tiết dự án."""
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = ProjectDetailScreen(self, user_info=user_info, logger=self.logger, project_id=project_id, app=self)
        # === THÊM DÒNG CÒN THIẾU TẠI ĐÂY ===
        # Hiển thị màn hình lên cửa sổ
        self.current_screen.pack(fill="both", expand=True)


if __name__ == "__main__":
    logger = log_setting(__name__)
    app = App(logger)
    app.mainloop()