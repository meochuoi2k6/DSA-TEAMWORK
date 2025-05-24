import tkinter as tk
from tkinter import messagebox
from frontend.screens.login_screen import LoginScreen
from frontend.screens.main_screen import MainScreen



    


def main():
    root = tk.Tk()
    root.title("Project Management Tool")
    root.geometry("800x600")

    def show_main_menu(username):
        login_frame = MainScreen(root, username)
        login_frame.pack()

    LoginScreen(root, show_main_menu)
    tk.mainloop()

if __name__ == "__main__":
    main()
        