# File: frontend/screens/main_screen.py

import customtkinter as ctk
import json
from datetime import datetime
from middleware import module_project
from frontend.CTkMessagebox import CTkMessagebox

class MainScreen(ctk.CTkFrame):
    def __init__(self, master, user_info, logger):
        super().__init__(master)
        self.app = master # Lưu lại tham chiếu đến app chính (master) để điều hướng
        self.user_info = user_info
        self.logger = logger
        self.pack(fill="both", expand=True)
        self.logger.info(f"Người dùng {self.user_info.get('name')} đã vào màn hình chính.")

        # Main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Project Manager", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Sidebar buttons
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Danh sách dự án", command=self.show_projects_list)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Thống kê")
        self.sidebar_button_3.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="Tạo project", command=self.open_create_project_form)
        self.sidebar_button_4.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 20))


        # Main content area
        self.main_content_frame = ctk.CTkFrame(self)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.display_area = ctk.CTkScrollableFrame(self.main_content_frame)
        self.display_area.pack(expand=True, fill="both")

        self.show_projects_list()
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def show_projects_list(self):
        for widget in self.display_area.winfo_children():
            widget.destroy()
        try:
            with open("data store/project.json", "r", encoding='utf-8') as f:
                projects = json.load(f)
            user_id = self.user_info.get("id")
            user_projects_found = False
            for project in projects:
                member_ids = [member['id'] for member in project.get("members", [])]
                if user_id in member_ids:
                    user_projects_found = True
                    project_card = ctk.CTkFrame(self.display_area, border_width=1, border_color="gray")
                    project_card.pack(fill="x", padx=10, pady=10)
                    info_frame = ctk.CTkFrame(project_card, fg_color="transparent")
                    info_frame.pack(fill="x", padx=10, pady=10)
                    info_frame.grid_columnconfigure(0, weight=1)
                    name_label = ctk.CTkLabel(info_frame, text=project.get("name", "Không có tên"), font=ctk.CTkFont(size=16, weight="bold"))
                    name_label.grid(row=0, column=0, sticky="w")
                    desc_label = ctk.CTkLabel(info_frame, text=project.get("description", ""), wraplength=500, justify="left")
                    desc_label.grid(row=1, column=0, sticky="w", pady=(5, 10))
                    id_label = ctk.CTkLabel(info_frame, text=f"ID: {project.get('projectID', '')} | Trạng thái: {project.get('status', '')}", font=ctk.CTkFont(size=10))
                    id_label.grid(row=2, column=0, sticky="w")
                    button_frame = ctk.CTkFrame(project_card, fg_color="transparent")
                    button_frame.pack(fill="x", padx=10, pady=(0, 10))
                    project_id = project.get("projectID")
                    delete_button = ctk.CTkButton(button_frame, text="Xóa", width=80, fg_color="red", hover_color="#C40000", command=lambda p_id=project_id: self.delete_project(p_id))
                    delete_button.pack(side="right", padx=(10, 0))
                    edit_button = ctk.CTkButton(button_frame, text="Sửa", width=80, command=lambda p_id=project_id: self.edit_project(p_id))
                    edit_button.pack(side="right", padx=(10, 0))
                    details_button = ctk.CTkButton(button_frame, text="Xem chi tiết", width=120, command=lambda p_id=project_id: self.view_project_details(p_id))
                    details_button.pack(side="right")
            if not user_projects_found:
                ctk.CTkLabel(self.display_area, text="Bạn chưa tham gia vào dự án nào.").pack(pady=20)
        except (FileNotFoundError, json.JSONDecodeError):
            ctk.CTkLabel(self.display_area, text="Chưa có dự án nào hoặc file dự án bị lỗi.").pack(pady=20)

    def open_create_project_form(self):
        form_window = ctk.CTkToplevel(self)
        form_window.title("Tạo Dự Án Mới")
        form_window.geometry("500x600")
        form_window.transient(self.winfo_toplevel())
        form_window.grab_set()
        name_label = ctk.CTkLabel(form_window, text="Tên dự án:")
        name_label.pack(padx=20, pady=(20, 5), anchor="w")
        name_entry = ctk.CTkEntry(form_window, width=460)
        name_entry.pack(padx=20, pady=5, fill="x")
        desc_label = ctk.CTkLabel(form_window, text="Mô tả:")
        desc_label.pack(padx=20, pady=5, anchor="w")
        desc_textbox = ctk.CTkTextbox(form_window, height=100)
        desc_textbox.pack(padx=20, pady=5, fill="both", expand=True)
        members_label = ctk.CTkLabel(form_window, text="Thêm thành viên:")
        members_label.pack(padx=20, pady=5, anchor="w")
        try:
            with open("data store/member.json", "r", encoding="utf-8") as f:
                all_members = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError): all_members = []
        scrollable_frame = ctk.CTkScrollableFrame(form_window, height=150)
        scrollable_frame.pack(padx=20, pady=5, fill="x")
        member_vars = {}
        for member in all_members:
            member_id = member.get("id")
            member_name = member.get("name")
            if member_id and member_name:
                var = ctk.StringVar(value="off")
                is_owner = (member_id == self.user_info.get("id"))
                checkbox = ctk.CTkCheckBox(scrollable_frame, text=f"{member_name} ({member_id})", variable=var, onvalue=member_id, offvalue="off")
                if is_owner:
                    checkbox.select()
                    checkbox.configure(state="disabled")
                checkbox.pack(anchor="w", padx=10)
                member_vars[member_id] = var
        def submit_project():
            project_name = name_entry.get()
            project_desc = desc_textbox.get("1.0", "end-1c")
            selected_members = [var.get() for var in member_vars.values() if var.get() != "off"]
            if not project_name:
                CTkMessagebox(title="Lỗi", message="Tên dự án không được để trống!", icon="cancel"); return
            if not selected_members:
                CTkMessagebox(title="Lỗi", message="Phải có ít nhất một thành viên!", icon="cancel"); return
            try:
                module_project.create_project(name=project_name, description=project_desc, ownerID=self.user_info.get("id"), startDate=datetime.now().strftime("%Y-%m-%d"), endDate="", status=0, memberID=selected_members)
                CTkMessagebox(title="Thành công", message=f"Đã tạo dự án '{project_name}' thành công!")
                form_window.destroy()
                self.show_projects_list()
            except Exception as e:
                self.logger.error(f"Lỗi khi tạo dự án: {e}")
                CTkMessagebox(title="Lỗi", message=f"Đã xảy ra lỗi khi tạo dự án:\n{e}", icon="cancel")
        button_frame = ctk.CTkFrame(form_window, fg_color="transparent")
        button_frame.pack(padx=20, pady=20, fill="x")
        cancel_button = ctk.CTkButton(button_frame, text="Hủy", command=form_window.destroy)
        cancel_button.pack(side="right")
        save_button = ctk.CTkButton(button_frame, text="Lưu Dự Án", command=submit_project)
        save_button.pack(side="right", padx=10)

    def view_project_details(self, project_id):
        self.logger.info(f"Yêu cầu xem chi tiết dự án: {project_id}")
        self.app.show_project_detail_screen(self.user_info, project_id)

    def edit_project(self, project_id):
        self.logger.info(f"Yêu cầu sửa dự án: {project_id}")
        CTkMessagebox(title="Thông báo", message=f"Tính năng 'Sửa' cho dự án {project_id} sẽ được phát triển!")

    def delete_project(self, project_id):
        self.logger.info(f"Yêu cầu xóa dự án: {project_id}")
        msg = CTkMessagebox(title="Xác nhận xóa", message=f"Bạn có chắc chắn muốn xóa dự án {project_id} không? Hành động này không thể hoàn tác.", icon="question", option_1="Hủy", option_2="Xóa")
        if msg.get() == "Xóa":
            try:
                module_project.delete_project(project_id)
                self.logger.warning(f"Người dùng đã xóa thành công dự án {project_id}")
                self.show_projects_list()
            except Exception as e:
                self.logger.error(f"Lỗi khi xóa dự án {project_id}: {e}")
                CTkMessagebox(title="Lỗi", message=f"Đã xảy ra lỗi khi xóa dự án:\n{e}", icon="cancel")

class AdminScreen(MainScreen):
    def __init__(self, master, user_info, logger):
        super().__init__(master, user_info, logger)
        self.logger.info(f"Admin {self.user_info.get('name')} đã vào màn hình chính.")
        self.logo_label.configure(text="Project Manager (Admin)")
        self.admin_button = ctk.CTkButton(self.sidebar_frame, text="Quản lý người dùng")
        self.admin_button.grid(row=4, column=0, padx=20, pady=10)

    def show_projects_list(self):
        for widget in self.display_area.winfo_children():
            widget.destroy()
        try:
            with open("data store/project.json", "r", encoding='utf-8') as f:
                projects = json.load(f)
            if not projects:
                ctk.CTkLabel(self.display_area, text="Chưa có dự án nào trong hệ thống.").pack(pady=20)
                return
            for project in projects:
                project_card = ctk.CTkFrame(self.display_area, border_width=1, border_color="gray")
                project_card.pack(fill="x", padx=10, pady=10)
                info_frame = ctk.CTkFrame(project_card, fg_color="transparent")
                info_frame.pack(fill="x", padx=10, pady=10)
                info_frame.grid_columnconfigure(0, weight=1)
                name_label = ctk.CTkLabel(info_frame, text=project.get("name", "Không có tên"), font=ctk.CTkFont(size=16, weight="bold"))
                name_label.grid(row=0, column=0, sticky="w")
                owner_label = ctk.CTkLabel(info_frame, text=f"Chủ sở hữu: {project.get('ownerID', 'N/A')}", font=ctk.CTkFont(size=11, slant="italic"))
                owner_label.grid(row=1, column=0, sticky="w")
                desc_label = ctk.CTkLabel(info_frame, text=project.get("description", ""), wraplength=500, justify="left")
                desc_label.grid(row=2, column=0, sticky="w", pady=(5, 10))
                id_label = ctk.CTkLabel(info_frame, text=f"ID: {project.get('projectID', '')} | Trạng thái: {project.get('status', '')}", font=ctk.CTkFont(size=10))
                id_label.grid(row=3, column=0, sticky="w")
                button_frame = ctk.CTkFrame(project_card, fg_color="transparent")
                button_frame.pack(fill="x", padx=10, pady=(0, 10))
                project_id = project.get("projectID")
                delete_button = ctk.CTkButton(button_frame, text="Xóa", width=80, fg_color="red", hover_color="#C40000", command=lambda p_id=project_id: self.delete_project(p_id))
                delete_button.pack(side="right", padx=(10, 0))
                edit_button = ctk.CTkButton(button_frame, text="Sửa", width=80, command=lambda p_id=project_id: self.edit_project(p_id))
                edit_button.pack(side="right", padx=(10, 0))
                details_button = ctk.CTkButton(button_frame, text="Xem chi tiết", width=120, command=lambda p_id=project_id: self.view_project_details(p_id))
                details_button.pack(side="right")
        except (FileNotFoundError, json.JSONDecodeError):
            ctk.CTkLabel(self.display_area, text="Chưa có dự án nào hoặc file dự án bị lỗi.").pack(pady=20)