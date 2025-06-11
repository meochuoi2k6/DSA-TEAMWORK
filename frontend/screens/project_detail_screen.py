# File: frontend/screens/project_detail_screen.py
import customtkinter as ctk
import json
from frontend.CTkMessagebox import CTkMessagebox
from middleware import module_project

class ProjectDetailScreen(ctk.CTkFrame):
    def __init__(self, master, user_info, logger, project_id, app):
        super().__init__(master)
        self.user_info = user_info
        self.logger = logger
        self.project_id = project_id
        self.app = app
        self.project_data = self.get_project_data()

        self.pack(fill="both", expand=True)
        self.logger.info(f"Đang xem chi tiết dự án: {self.project_id}")

        if not self.project_data:
            ctk.CTkLabel(self, text=f"Lỗi: Không tìm thấy dữ liệu cho dự án ID: {self.project_id}").pack(pady=20)
            ctk.CTkButton(self, text="Quay lại", command=self.go_back).pack(pady=10)
            return
            
        self.create_widgets()

    def get_project_data(self):
        try:
            with open("data store/project.json", "r", encoding="utf-8") as f:
                projects = json.load(f)
            for project in projects:
                if project.get("projectID") == self.project_id:
                    return project
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Lỗi khi đọc file dự án: {e}")
        return None

    def refresh_data_and_widgets(self):
        """Tải lại dữ liệu dự án và vẽ lại các widget."""
        self.project_data = self.get_project_data()
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def go_back(self):
        self.app.show_main_menu(self.user_info)

    def open_add_task_form(self):
        form_window = ctk.CTkToplevel(self)
        form_window.title("Thêm Task Mới")
        form_window.geometry("400x400")
        form_window.transient(self.winfo_toplevel())
        form_window.grab_set()

        title_label = ctk.CTkLabel(form_window, text="Tiêu đề Task:")
        title_label.pack(padx=20, pady=(20, 5), anchor="w")
        title_entry = ctk.CTkEntry(form_window, width=360)
        title_entry.pack(padx=20, pady=5, fill="x")

        desc_label = ctk.CTkLabel(form_window, text="Mô tả:")
        desc_label.pack(padx=20, pady=5, anchor="w")
        desc_textbox = ctk.CTkTextbox(form_window, height=100)
        desc_textbox.pack(padx=20, pady=5, fill="both", expand=True)

        def submit_add_task():
            task_title = title_entry.get()
            task_desc = desc_textbox.get("1.0", "end-1c")

            if not task_title:
                CTkMessagebox(title="Lỗi", message="Tiêu đề task không được để trống!", icon="cancel")
                return
            
            try:
                module_project.add_task(
                    project_id=self.project_id,
                    title=task_title,
                    description=task_desc,
                    assignee_id=""
                )
                self.logger.info(f"Đã thêm task '{task_title}' vào dự án {self.project_id}")
                CTkMessagebox(title="Thành công", message="Đã thêm task mới thành công!")
                form_window.destroy()
                self.refresh_data_and_widgets()
            except Exception as e:
                self.logger.error(f"Lỗi khi thêm task: {e}")
                CTkMessagebox(title="Lỗi", message=f"Đã có lỗi xảy ra:\n{e}", icon="cancel")

        button_frame = ctk.CTkFrame(form_window, fg_color="transparent")
        button_frame.pack(padx=20, pady=20, fill="x")
        
        cancel_button = ctk.CTkButton(button_frame, text="Hủy", command=form_window.destroy)
        cancel_button.pack(side="right")

        save_button = ctk.CTkButton(button_frame, text="Lưu Task", command=submit_add_task)
        save_button.pack(side="right", padx=10)

    def on_status_change(self, new_status: str, task_id: str):
        try:
            self.logger.info(f"Người dùng thay đổi trạng thái của task {task_id} thành {new_status}")
            module_project.update_task_status(self.project_id, task_id, new_status)
            # Sau khi thay đổi, cập nhật lại project_data để UI phản ánh đúng (nếu cần)
            # Tuy nhiên, combobox đã tự cập nhật hiển thị, nên chỉ cần dữ liệu nền đúng là được.
            # self.project_data = self.get_project_data() 
        except Exception as e:
            self.logger.error(f"Lỗi khi cập nhật trạng thái task: {e}")
            CTkMessagebox(title="Lỗi", message="Không thể cập nhật trạng thái task!", icon="cancel")
            self.refresh_data_and_widgets()

    def create_widgets(self):
        if not self.project_data: return

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=10)
        
        back_button = ctk.CTkButton(top_frame, text="< Quay lại danh sách", command=self.go_back)
        back_button.pack(side="left")

        add_task_button = ctk.CTkButton(top_frame, text="+ Thêm Task Mới", command=self.open_add_task_form)
        add_task_button.pack(side="right")

        project_info_frame = ctk.CTkFrame(self)
        project_info_frame.pack(fill="x", padx=20, pady=10)
        
        name_label = ctk.CTkLabel(project_info_frame, text=self.project_data.get("name", ""), font=ctk.CTkFont(size=24, weight="bold"))
        name_label.pack(pady=(10, 5), padx=20)
        desc_label = ctk.CTkLabel(project_info_frame, text=self.project_data.get("description", ""), wraplength=600, justify="left")
        desc_label.pack(pady=5, padx=20)

        tasks_container = ctk.CTkFrame(self)
        tasks_container.pack(fill="both", expand=True, padx=20, pady=10)

        tasks_header_label = ctk.CTkLabel(tasks_container, text="Danh sách công việc", font=ctk.CTkFont(size=18, weight="bold"))
        tasks_header_label.pack(pady=10)

        tasks_scroll_frame = ctk.CTkScrollableFrame(tasks_container)
        tasks_scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        tasks = self.project_data.get("tasks", [])
        if not tasks:
            ctk.CTkLabel(tasks_scroll_frame, text="Chưa có công việc nào trong dự án này.").pack(pady=20)
        else:
            for task in tasks:
                task_card = ctk.CTkFrame(tasks_scroll_frame, border_width=1)
                task_card.pack(fill="x", padx=5, pady=5)
                task_card.grid_columnconfigure(0, weight=1)

                task_title = ctk.CTkLabel(task_card, text=task.get("title", "Không có tiêu đề"), font=ctk.CTkFont(weight="bold"))
                task_title.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 5))

                status_frame = ctk.CTkFrame(task_card, fg_color="transparent")
                status_frame.grid(row=0, column=1, sticky="e", padx=10, pady=(5,5))

                task_id = task.get("taskID")
                status_options = ["Todo", "In Progress", "Done"]
                status_combobox = ctk.CTkComboBox(status_frame, values=status_options,
                                                    command=lambda choice, t_id=task_id: self.on_status_change(choice, t_id))
                status_combobox.set(task.get("status", "Todo"))
                status_combobox.pack()