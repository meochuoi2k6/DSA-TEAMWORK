import logging
import tkinter as tk

class GuiLogHandler(logging.Handler):
    def __init__(self, text_widget: tk.Text):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)

        def append():
            # Kiểm tra widget còn tồn tại và chưa bị hủy
            if self.text_widget is None:
                return
            if not self.text_widget.winfo_exists():
                return
            try:
                self.text_widget.configure(state='normal')
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)
                self.text_widget.configure(state='disabled')
            except tk.TclError:
                pass  # Widget đã bị destroy

        try:
            if self.text_widget is not None and self.text_widget.winfo_exists():
                self.text_widget.after(0, append)
        except tk.TclError:
            pass
    def destroy(self):
        self.text_widget = None
        self.setLevel(logging.NOTSET)
