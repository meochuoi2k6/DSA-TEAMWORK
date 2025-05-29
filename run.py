import tkinter as tk
from tkinter import scrolledtext
from frontend.screens.login_screen import LoginScreen
from frontend.screens.main_screen import MainScreen
from middleware.log import log_setting
from middleware.GuiLogHandler import GuiLogHandler
from frontend.screens.logScreen import show_log_window

logger = log_setting(__name__)

def main():

    root = tk.Tk()
    root.title("Project Management Tool")
    root.geometry("800x800")

    # Hiển thị cửa sổ Log Screen
    show_log_window(logger)
    logger.info("Khởi động ứng dụng thành công")
    def show_main_menu(username):
        main_frame = MainScreen(root, username)
        main_frame.pack()

    LoginScreen(root, show_main_menu)
    root.mainloop()

if __name__ == "__main__":
    main()