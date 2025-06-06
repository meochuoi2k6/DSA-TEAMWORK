from customtkinter import *
from frontend.screens.login_screen import LoginPage
from frontend.screens.main_screen import MainScreen
from middleware.log import log_setting
from middleware.GuiLogHandler import GuiLogHandler
from frontend.screens.logScreen import show_log_window

logger = log_setting(__name__)

def main():

    root = CTk(fg_color="black")
    root.title("Project Management Tool")
    

    # Hiển thị cửa sổ Log Screen
    
    
    #root.iconbitmap(os.path.join(image_path, "logo.ico"))
    def show_main_menu(username):
        main_frame = MainScreen(root, username)
        main_frame.pack()
        # Hiển thị cửa sổ Log Screen
        show_log_window(logger)

    LoginPage(root, show_main_menu)
    logger.info("Khởi động ứng dụng thành công")
    root.mainloop()

if __name__ == "__main__":
    main()