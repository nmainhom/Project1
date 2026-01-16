"""
Module vẽ và hiển thị bản đồ
"""
import tkinter as tk


class MapRenderer:
    """Class xử lý việc vẽ bản đồ"""
    
    def __init__(self, canvas, location_data, distance_matrix, image_manager):
        """
        Khởi tạo MapRenderer
        
        Args:
            canvas: Canvas để vẽ
            location_data: Instance của LocationData
            distance_matrix: Instance của DistanceMatrix
            image_manager: Instance của ImageManager
        """
        self.canvas = canvas
        self.location_data = location_data
        self.distance_matrix = distance_matrix
        self.image_manager = image_manager
        
        # Callback khi click vào location
        self.on_location_click = None
        
        # Bind click event
        self.canvas.bind("<Button-1>", self._handle_click)
        
        # Lưu vị trí các nodes để detect click
        self.node_positions = {}
    
    def _handle_click(self, event):
        """
        Xử lý sự kiện click trên canvas
        
        Args:
            event: Tkinter event object
        """
        # Tìm node gần nhất với vị trí click
        click_x, click_y = event.x, event.y
        clicked_node = None
        min_distance = float('inf')
        
        for loc_id, (x, y) in self.node_positions.items():
            # Tính khoảng cách từ click đến tâm node
            distance = ((click_x - x) ** 2 + (click_y - y) ** 2) ** 0.5
            
            # Nếu click trong vòng bán kính 40px của node
            if distance <= 40 and distance < min_distance:
                min_distance = distance
                clicked_node = loc_id
        
        # Gọi callback nếu có
        if clicked_node and self.on_location_click:
            self.on_location_click(clicked_node)
    
    def draw_map(self, selected_locations, path_result=None, start_location=None,
                 mandatory_locations=None):
        
        if mandatory_locations is None:
            mandatory_locations = []
        
        self.canvas.delete("all")
        self.node_positions.clear()
        
        if not selected_locations:
            # Hiển thị hướng dẫn
            self.canvas.create_text(350, 250,
                                   text="📍 Vui lòng chọn địa điểm từ danh sách\n\n"
                                        "💡 Click điểm đầu tiên = Điểm bắt đầu\n"
                                        "   Click các điểm khác = Điểm BẮT BUỘC",
                                   font=("Arial", 14), fill="#6b7280",
                                   justify=tk.CENTER)
            return
        
        # Lấy danh sách tất cả các nodes cần hiển thị
        nodes_to_display = set(selected_locations)
        intermediate_nodes = []
        exceeded_nodes = []
        
        # Nếu có path result, thêm tất cả nodes trong path
        if path_result:
            path = path_result[0]
            if len(path_result) >= 3:
                intermediate_nodes = path_result[2]
            if len(path_result) >= 4:
                exceeded_nodes = path_result[3]
            nodes_to_display.update(path)
        
        # Vẽ các edges
        self.draw_edges(nodes_to_display)
        
        # Vẽ path nếu có
        if path_result:
            self.draw_path(path_result[0])
        
        # Vẽ các địa điểm
        self.draw_locations(nodes_to_display, selected_locations, 
                          intermediate_nodes, path_result, start_location,
                          mandatory_locations, exceeded_nodes)
    
    def draw_edges(self, nodes_to_display):
        """
        Vẽ các cạnh kết nối giữa các địa điểm
        
        Args:
            nodes_to_display: Set các node cần hiển thị
        """
        locations = self.location_data.get_all_locations()
        distances = self.distance_matrix.get_all_distances()
        drawn_edges = set()
        
        for loc1 in nodes_to_display:
            for loc2 in nodes_to_display:
                edge = tuple(sorted([loc1, loc2]))
                if edge in distances and edge not in drawn_edges:
                    drawn_edges.add(edge)
                    
                    x1 = locations[loc1]["x"]
                    y1 = locations[loc1]["y"]
                    x2 = locations[loc2]["x"]
                    y2 = locations[loc2]["y"]
                    
    def draw_path(self, path):
        """
        Vẽ đường đi (path) bằng mũi tên màu đỏ
        
        Args:
            path: Danh sách các địa điểm theo thứ tự
        """
        locations = self.location_data.get_all_locations()
        
        for i in range(len(path) - 1):
            loc1, loc2 = path[i], path[i + 1]
            x1 = locations[loc1]["x"]
            y1 = locations[loc1]["y"]
            x2 = locations[loc2]["x"]
            y2 = locations[loc2]["y"]
            
            # Vẽ đường đi với mũi tên
            self.canvas.create_line(x1, y1, x2, y2,
                                   width=5, fill="#dc2626",
                                   arrow=tk.LAST, arrowshape=(12, 15, 5))
    
    def draw_locations(self, nodes_to_display, selected_locations, 
                      intermediate_nodes, path_result, start_location=None,
                      mandatory_locations=None, exceeded_nodes=None):
        """
        Vẽ các địa điểm trên bản đồ (UPDATED!)
        
        Args:
            nodes_to_display: Set các node cần hiển thị
            selected_locations: Danh sách địa điểm đã chọn
            intermediate_nodes: Danh sách điểm trung gian
            path_result: Tuple (path, distance, intermediate) hoặc None
            start_location: ID của điểm bắt đầu
            mandatory_locations: Danh sách điểm bắt buộc
            exceeded_nodes: Danh sách điểm bị bỏ qua
        """
        if mandatory_locations is None:
            mandatory_locations = []
        if exceeded_nodes is None:
            exceeded_nodes = []
        
        locations = self.location_data.get_all_locations()
        
        for loc_id in nodes_to_display:
            x = locations[loc_id]["x"]
            y = locations[loc_id]["y"]
            
            # Lưu vị trí node
            self.node_positions[loc_id] = (x, y)
            
            # Vẽ hình ảnh
            img = self.image_manager.get_image(f"{loc_id}_map")
            if img:
                self.canvas.create_image(x, y, image=img)
            
            # Xác định trạng thái
            in_path = path_result and loc_id in path_result[0]
            is_intermediate = loc_id in intermediate_nodes
            is_selected = loc_id in selected_locations
            is_start = loc_id == start_location
            is_mandatory = loc_id in mandatory_locations
            is_exceeded = loc_id in exceeded_nodes
            
            # Logic màu sắc mới
            if is_exceeded:
                # Điểm bị bỏ qua: border xám mờ
                color = "#9ca3af"
                width = 2
            elif is_start and not in_path:
                # Điểm bắt đầu được chọn nhưng chưa tìm đường
                color = "#dc2626"
                width = 6
                # Thêm hiệu ứng glow
                self.canvas.create_oval(x - 45, y - 45, x + 45, y + 45,
                                       outline="#fca5a5", width=3)
            elif in_path:
                if is_intermediate:
                    # Node trung gian: border cam
                    color = "#f97316"
                    width = 4
                elif is_start:
                    # Điểm bắt đầu trong path: border đỏ rất đậm
                    color = "#dc2626"
                    width = 6
                elif is_mandatory:
                    # Điểm bắt buộc trong path: border vàng đậm
                    color = "#eab308"
                    width = 5
                else:
                    # Node được chọn trong path: border xanh
                    color = "#3b82f6"
                    width = 4
            else:
                # Node được chọn nhưng không trong path
                if is_mandatory:
                    # Điểm bắt buộc: border vàng
                    color = "#fbbf24"
                    width = 4
                else:
                    # Điểm tùy chọn: border xanh nhạt
                    color = "#60a5fa"
                    width = 3
            
            # Vẽ border
            self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40,
                                   outline=color, width=width)
            
            # Badge "START" cho điểm bắt đầu
            if is_start and not in_path:
                self.canvas.create_rectangle(x - 30, y - 55, x + 30, y - 40,
                                            fill="#dc2626", outline="white", width=2)
                self.canvas.create_text(x, y - 47.5, text="START",
                                       font=("Arial", 9, "bold"), fill="white")
            
            # Badge "MUST" cho điểm bắt buộc
            if is_mandatory and not is_start and not in_path:
                self.canvas.create_rectangle(x - 30, y - 55, x + 30, y - 40,
                                            fill="#eab308", outline="white", width=2)
                self.canvas.create_text(x, y - 47.5, text="MUST",
                                       font=("Arial", 9, "bold"), fill="white")
            
            # Badge "SKIP" cho điểm bị bỏ qua
            if is_exceeded:
                self.canvas.create_rectangle(x - 30, y - 55, x + 30, y - 40,
                                            fill="#9ca3af", outline="white", width=2)
                self.canvas.create_text(x, y - 47.5, text="SKIP",
                                       font=("Arial", 9, "bold"), fill="white")
            
            # Số thứ tự nếu trong path
            if in_path and not is_exceeded:
                order = path_result[0].index(loc_id) + 1
                
                if is_intermediate:
                    badge_color = "#f97316"
                elif is_mandatory:
                    badge_color = "#eab308"
                elif is_start:
                    badge_color = "#dc2626"
                else:
                    badge_color = "#3b82f6"
                
                # Vẽ badge số thứ tự
                if is_start:
                    self.canvas.create_oval(x + 23, y - 27, x + 47, y - 3,
                                           fill=badge_color, outline="white", width=3)
                    self.canvas.create_text(x + 35, y - 15, text=str(order),
                                           font=("Arial", 14, "bold"), fill="white")
                else:
                    self.canvas.create_oval(x + 25, y - 25, x + 45, y - 5,
                                           fill=badge_color, outline="white", width=2)
                    self.canvas.create_text(x + 35, y - 15, text=str(order),
                                           font=("Arial", 12, "bold"), fill="white")
            
            # Tên địa điểm
            name = locations[loc_id]["name"]
            
            # Xác định màu nền
            if is_exceeded:
                bg_color = "#f3f4f6"  # Xám nhạt
            elif is_intermediate:
                bg_color = "#fff7ed"  # Cam nhạt
            elif is_mandatory:
                bg_color = "#fef3c7"  # Vàng nhạt
            elif is_start:
                bg_color = "#fee2e2"  # Đỏ nhạt
            else:
                bg_color = "white"
            
            self.canvas.create_rectangle(x - 60, y + 45, x + 60, y + 65,
                                        fill=bg_color, outline="#d1d5db")
            self.canvas.create_text(x, y + 55, text=name,
                                   font=("Arial", 9, "bold"), fill="#1f2937")