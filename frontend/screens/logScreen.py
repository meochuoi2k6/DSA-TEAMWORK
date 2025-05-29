import tkinter as tk
from tkinter import scrolledtext
import logging
from middleware.GuiLogHandler import GuiLogHandler
def show_log_window(logger: logging.Logger):
    log_win = tk.Toplevel()
    log_win.title("Log Viewer")
    log_win.geometry("600x400")
    
    log_area = tk.Text(
        log_win, state='disabled',
        bg = "black",
        fg = "lime",
        font = ("Consolas", 10),
        insertbackground='white'
        )
    log_area.pack(expand=True, fill="both")

    gui_handler = GuiLogHandler(log_area)
    gui_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s'))
    gui_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(gui_handler)

    logger.setLevel(logging.DEBUG)
