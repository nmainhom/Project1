"""
Module chứa các thành phần giao diện người dùng
"""
import tkinter as tk
from tkinter import ttk, messagebox


class TourismUI:
    """Class quản lý giao diện người dùng"""
    
    def __init__(self, root, location_data):
        
        self.root = root
        self.location_data = location_data
        
        # Biến UI
        self.district_var = None
        self.scrollable_frame = None
        self.location_canvas = None
        self.stats_label = None
        self.result_label = None
        self.result_scrollable_frame = None
        self.map_canvas = None
        self.limit_var = None
        self.limit_entry = None
        
        # Callbacks
        self.on_location_toggle = None
        self.on_district_change_callback = None
        self.on_find_path = None
        self.on_reset = None
    
    def create_ui(self):
        """Tạo toàn bộ giao diện"""
        self._create_title()
        self._create_main_container()
    
    def _create_title(self):
        """Tạo tiêu đề ứng dụng"""
        title_frame = tk.Frame(self.root, bg="#0ea5e9", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame,
                              text=" HỆ THỐNG TƯ VẤN DU LỊCH HÀ NỘI",
                              font=("Arial", 18, "bold"),
                              bg="#0ea5e9", fg="white")
        title_label.pack(pady=15)
    
    def _create_main_container(self):
        """Tạo container chính"""
        main_container = tk.Frame(self.root, bg="#c7ecfe")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tạo cột trái và phải
        self._create_left_column(main_container)
        self._create_right_panel(main_container)
    
    def _create_left_column(self, parent):
        """Tạo cột trái (danh sách địa điểm + điều khiển)"""
        left_column = tk.Frame(parent, bg="white", width=350)
        left_column.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_column.pack_propagate(False)
        
        # Phần danh sách địa điểm
        self._create_location_list_panel(left_column)
        
        # Phần điều khiển
        self._create_control_panel(left_column)
    
    def _create_location_list_panel(self, parent):
        """Tạo panel danh sách địa điểm"""
        left_panel = tk.Frame(parent, bg="white", height=550)
        left_panel.pack(side=tk.TOP, fill=tk.X)
        left_panel.pack_propagate(False)
        
        # Header
        header = tk.Frame(left_panel, bg="#0ea5e9", height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text=" DANH SÁCH ĐỊA ĐIỂM",
                font=("Arial", 12, "bold"),
                bg="#0ea5e9", fg="white").pack(pady=10)
        
        # Bộ lọc quận
        self._create_district_filter(left_panel)
        
        # Frame cuộn
        self._create_scrollable_list(left_panel)
    
    def _create_district_filter(self, parent):
        """Tạo bộ lọc theo quận"""
        filter_frame = tk.Frame(parent, bg="white")
        filter_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(filter_frame, text="Lọc theo quận:",
                font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=5)
        
        self.district_var = tk.StringVar(value="Tất cả")
        district_combo = ttk.Combobox(filter_frame,
                                     textvariable=self.district_var,
                                     values=self.location_data.get_districts(),
                                     state="readonly",
                                     width=15)
        district_combo.pack(side=tk.LEFT, padx=5)
        district_combo.bind("<<ComboboxSelected>>", 
                          lambda e: self._on_district_change())
    
    def _create_scrollable_list(self, parent):
        """Tạo danh sách cuộn được"""
        scroll_frame = tk.Frame(parent, bg="white")
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        canvas = tk.Canvas(scroll_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", 
                                 command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Hỗ trợ cuộn bằng chuột
        def left_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", 
                                                         left_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        self.location_canvas = canvas
    
    def _create_control_panel(self, parent):
        """Tạo bảng điều khiển với ô nhập giới hạn và 2 nút bấm"""
        control_frame = tk.LabelFrame(parent, text="YÊU CẦU", font=("Arial", 12, "bold"),
                                    bg="#f8fafc", fg="#0369a1", padx=10, pady=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # --- HÀNG 1: Ô nhập giới hạn ---
        input_frame = tk.Frame(control_frame, bg="#f8fafc")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(input_frame, text="Giới hạn (km):", font=("Arial", 10), 
                bg="#f8fafc").pack(side=tk.LEFT)
        
        self.limit_var = tk.StringVar(value="") # Mặc định để trống
        self.limit_entry = tk.Entry(input_frame, textvariable=self.limit_var, 
                                    font=("Arial", 10), width=15)
        self.limit_entry.pack(side=tk.LEFT, padx=10)
        
        # --- HÀNG 2: Hai nút bấm Tìm đường và Đặt lại ---
        button_row = tk.Frame(control_frame, bg="#f8fafc")
        button_row.pack(fill=tk.X)
        
        # Nút Tìm Đường (Bo góc giả lập bằng cách dùng flat relief và padx/pady)
        self.find_btn = tk.Button(button_row, text="TÌM ĐƯỜNG", 
                                font=("Arial", 10, "bold"),
                                bg="#10b981", fg="white", 
                                activebackground="#059669",
                                cursor="hand2", bd=0, padx=15, pady=8,
                                command=self._on_find_path_click)
        self.find_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        # Nút Đặt Lại
        self.reset_btn = tk.Button(button_row, text="ĐẶT LẠI", 
                                font=("Arial", 10, "bold"),
                                bg="#ef4444", fg="white", 
                                activebackground="#dc2626",
                                cursor="hand2", bd=0, padx=15, pady=8,
                                command=self._on_reset_click)
        self.reset_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
        # Thống kê
        stats_frame = tk.Frame(control_frame, bg="white")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        self.stats_label = tk.Label(stats_frame,
                                    text="Chưa có địa điểm nào được chọn",
                                    font=("Arial", 9),
                                    bg="white",
                                    fg="#6b7280",
                                    justify=tk.LEFT,
                                    anchor="nw")
        self.stats_label.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def _on_find_path_click(self):
        """Xử lý khi click nút tìm đường"""
        limit_val = self.limit_var.get().strip()
        if self.on_find_path:
            if limit_val == "":
                self.on_find_path(None)
            else:
                try:
                    limit = float(limit_val)
                    self.on_find_path(limit)
                except ValueError:
                    messagebox.showerror("Lỗi", "Vui lòng nhập số km hợp lệ!")
    
    def _create_right_panel(self, parent):
        """Tạo panel bên phải (kết quả + bản đồ)"""
        right_panel = tk.Frame(parent, bg="white")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Kết quả
        self._create_result_frame(right_panel)
        
        # Bản đồ
        self._create_map_frame(right_panel)
    
    def _create_result_frame(self, parent):
        """Tạo khung hiển thị kết quả"""
        result_outer = tk.Frame(parent, bg="#ecfdf5", height=150)
        result_outer.pack(fill=tk.X, padx=10, pady=(0, 10))
        result_outer.pack_propagate(False)
        
        # Header
        result_header = tk.Frame(result_outer, bg="#059669", height=35)
        result_header.pack(fill=tk.X)
        result_header.pack_propagate(False)
        tk.Label(result_header, text="✓ KẾT QUẢ TÌM ĐƯỜNG",
                font=("Arial", 11, "bold"),
                bg="#059669", fg="white").pack(pady=8)
        
        # Scrollable result
        result_scroll_frame = tk.Frame(result_outer, bg="#ecfdf5")
        result_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        canvas_result = tk.Canvas(result_scroll_frame, bg="#ecfdf5", 
                                 highlightthickness=0)
        scrollbar_result = ttk.Scrollbar(result_scroll_frame, orient="vertical",
                                        command=canvas_result.yview)
        
        self.result_scrollable_frame = tk.Frame(canvas_result, bg="#ecfdf5")
        
        self.result_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_result.configure(scrollregion=canvas_result.bbox("all"))
        )
        
        canvas_result.create_window((0, 0), window=self.result_scrollable_frame,
                                   anchor="nw")
        
        self.result_label = tk.Label(
            self.result_scrollable_frame,
            text=" Chọn địa điểm và nhấn 'Tìm Đường'\n\n"
                 " Tip: Click điểm đầu tiên trên bản đồ = Điểm bắt đầu\n"
                 "      Click các điểm khác = Điểm BẮT BUỘC phải đi!",
            font=("Arial", 10),
            bg="#ecfdf5",
            fg="#374151",
            justify=tk.LEFT,
            wraplength=400,
            anchor="nw"
        )
        self.result_label.pack(fill=tk.X, pady=5)
        
        canvas_result.configure(yscrollcommand=scrollbar_result.set)
        
        canvas_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_result.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Hỗ trợ cuộn chuột
        def result_mousewheel(event):
            canvas_result.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas_result.bind("<Enter>", 
                          lambda e: canvas_result.bind_all("<MouseWheel>", 
                                                           result_mousewheel))
        canvas_result.bind("<Leave>", 
                          lambda e: canvas_result.unbind_all("<MouseWheel>"))
    
    def _create_map_frame(self, parent):
        """Tạo khung bản đồ"""
        map_frame = tk.Frame(parent, bg="white", relief=tk.SUNKEN, bd=2)
        map_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.map_canvas = tk.Canvas(map_frame, bg="#e0f2fe", 
                                    highlightthickness=0)
        self.map_canvas.pack(fill=tk.BOTH, expand=True)
    
    def create_location_list(self, selected_locations, start_location=None, 
                            mandatory_locations=None):
        
        if mandatory_locations is None:
            mandatory_locations = []
        
        # Xóa các widget cũ
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Lọc địa điểm theo quận
        district_filter = self.district_var.get()
        filtered_locations = self.location_data.get_locations_by_district(
            district_filter
        )
        
        if not filtered_locations:
            tk.Label(self.scrollable_frame,
                    text="Không có địa điểm nào",
                    font=("Arial", 10),
                    bg="white", fg="#6b7280").pack(pady=20)
            return
        
        # Tạo card cho mỗi địa điểm
        for loc_id, loc_data in filtered_locations.items():
            self._create_location_card(loc_id, loc_data, selected_locations,
                                      start_location, mandatory_locations)
    
    def _create_location_card(self, loc_id, loc_data, selected_locations,
                             start_location, mandatory_locations):
        """Tạo card cho một địa điểm (UPDATED!)"""
        is_selected = loc_id in selected_locations
        is_start = loc_id == start_location
        is_mandatory = loc_id in mandatory_locations
        
        # Xác định màu nền
        if is_start:
            bg_color = "#fee2e2"  # Đỏ nhạt cho điểm bắt đầu
        elif is_mandatory:
            bg_color = "#fef3c7"  # Vàng nhạt cho điểm bắt buộc
        elif is_selected:
            bg_color = "#dbeafe"  # Xanh nhạt cho điểm đã chọn
        else:
            bg_color = "#f9fafb"  # Xám nhạt cho điểm chưa chọn
        
        card = tk.Frame(self.scrollable_frame,
                       bg=bg_color,
                       relief=tk.RAISED if is_selected else tk.FLAT,
                       bd=2)
        card.pack(fill=tk.X, padx=5, pady=5)
        
        # Nội dung
        content = tk.Frame(card, bg=bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header với icon và trạng thái
        header = tk.Frame(content, bg=bg_color)
        header.pack(fill=tk.X)
        
        # Icon
        if is_start:
            icon = "🚩"
            status = " (ĐIỂM BẮT ĐẦU)"
        elif is_mandatory:
            icon = "⭐"
            status = " (BẮT BUỘC)"
        elif is_selected:
            icon = "✅"
            status = " (Tùy chọn)"
        else:
            icon = "📍"
            status = ""
        
        tk.Label(header, text=icon,
                font=("Arial", 12), bg=bg_color).pack(side=tk.LEFT)
        
        tk.Label(header, text=loc_data["name"] + status,
                font=("Arial", 11, "bold"),
                bg=bg_color, fg="#1f2937").pack(side=tk.LEFT, padx=5)
        
        # Quận
        tk.Label(content, text=f" {loc_data['district']}",
                font=("Arial", 9),
                bg=bg_color, fg="#6b7280").pack(anchor="w", pady=2)
        
        # Mô tả
        tk.Label(content, text=loc_data["description"],
                font=("Arial", 9, "italic"),
                bg=bg_color, fg="#374151",
                wraplength=280, justify=tk.LEFT).pack(anchor="w", pady=2)
        
        # Nút chọn/bỏ chọn
        btn_text = "Bỏ chọn" if is_selected else "Chọn địa điểm"
        btn_color = "#ef4444" if is_selected else "#3b82f6"
        
        btn = tk.Button(content,
                       text=btn_text,
                       font=("Arial", 9, "bold"),
                       bg=btn_color, fg="white",
                       cursor="hand2",
                       command=lambda: self._on_location_toggle(loc_id))
        btn.pack(fill=tk.X, pady=(5, 0))
    
    def update_stats(self, selected_locations, start_location=None, 
                    mandatory_locations=None):
        
        if not selected_locations:
            self.stats_label.config(
                text="Chưa có địa điểm nào được chọn",
                fg="#6b7280"
            )
            return
        
        # Thống kê
        locations = self.location_data.get_all_locations()
        
        
        stats_text = f"   Tổng: {len(selected_locations)} địa điểm\n"
        
        if start_location:
            start_name = locations[start_location]["name"]
        
        optional_count = len(selected_locations) - len(mandatory_locations)
        
        self.stats_label.config(text=stats_text, fg="#1f2937")
    def display_result(self, path_result, start_location=None, 
                      mandatory_locations=None):
        
        if not path_result:
            return
        
        if mandatory_locations is None:
            mandatory_locations = []
        
        path, total_distance, intermediate_locations, exceeded_locations = path_result
        locations = self.location_data.get_all_locations()
        
        # Format kết quả
        result_text = f" Tìm thấy đường đi tối ưu!\n"
        result_text += f" Tổng quãng đường: {total_distance:.2f} km\n"
        result_text += f" Số điểm đi qua: {len(path)} điểm\n"
        
        if start_location:
            start_name = locations[start_location]["name"]
            result_text += f" Xuất phát từ: {start_name}\n"
        
        if exceeded_locations:
            result_text += f" Bỏ qua: {len(exceeded_locations)} điểm (vượt giới hạn)\n"
        
        result_text += "\n Lộ trình:\n"
        
        for i, loc_id in enumerate(path, 1):
            loc_name = locations[loc_id]["name"]
            is_intermediate = loc_id in intermediate_locations
            is_start = loc_id == start_location
            is_mandatory = loc_id in mandatory_locations
            
            if is_start:
                result_text += f"{i}.  {loc_name} (Bắt đầu)\n"
            elif is_mandatory:
                result_text += f"{i}.  {loc_name} (Bắt buộc)\n"
            elif is_intermediate:
                result_text += f"{i}.  {loc_name} (Trung gian)\n"
            else:
                result_text += f"{i}.  {loc_name} (Tùy chọn)\n"
        
        if intermediate_locations:
            result_text += "\n Gợi ý: Trên đường đi sẽ đi qua:\n"
            for loc_id in intermediate_locations:
                loc_name = locations[loc_id]["name"]
                result_text += f"  • {loc_name}\n"
        
        if exceeded_locations:
            result_text += "\n Các điểm bị bỏ qua:\n"
            for loc_id in exceeded_locations:
                loc_name = locations[loc_id]["name"]
                result_text += f"  • {loc_name}\n"
        
        self.result_label.config(text=result_text, fg="#16a34a")
    
    def reset_result_display(self):
        """Reset hiển thị kết quả"""
        self.result_label.config(
            text=" Chọn địa điểm và nhấn 'Tìm Đường'\n\n"
                 " Tip: Click điểm đầu tiên trên bản đồ = Điểm bắt đầu\n"
                 "      Click các điểm khác = Điểm BẮT BUỘC phải đi!",
            fg="#374151"
        )
    
    # Callback handlers
    def _on_location_toggle(self, loc_id):
        """Xử lý khi toggle địa điểm"""
        if self.on_location_toggle:
            self.on_location_toggle(loc_id)
    
    def _on_district_change(self):
        """Xử lý khi thay đổi quận"""
        if self.on_district_change_callback:
            self.on_district_change_callback()
    
    def _on_reset_click(self):
        """Xử lý khi click nút reset"""
        if self.on_reset:
            self.on_reset()