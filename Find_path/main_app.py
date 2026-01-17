import tkinter as tk
from tkinter import messagebox, simpledialog

from data_model import LocationData, DistanceMatrix
from path_finder import PathFinder
from image_handler import ImageManager
from map_renderer import MapRenderer
from ui_components import TourismUI


class HanoiTourismApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Du Lịch Hà Nội")
        self.root.geometry("1400x800")
        self.root.configure(bg="#c7ecfe")
        
        # Khởi tạo các module
        self.location_data = LocationData()
        self.distance_matrix = DistanceMatrix()
        self.path_finder = PathFinder(self.location_data, self.distance_matrix)
        self.image_manager = ImageManager()
        
        # State
        self.selected_locations = []  # Danh sách địa điểm đã chọn (cả bắt buộc và optional)
        self.start_location = None  # Điểm bắt đầu
        self.mandatory_locations = []  # Danh sách điểm BẮT BUỘC phải đi 
        self.path_result = None  # Kết quả tìm đường
        
        # Khởi tạo UI
        self.ui = TourismUI(self.root, self.location_data)
        
        # Set up callbacks cho UI
        self._setup_callbacks()
        
        # Tạo giao diện
        self.ui.create_ui()
        
        # Khởi tạo MapRenderer sau khi có canvas
        self.map_renderer = MapRenderer(
            self.ui.map_canvas,
            self.location_data,
            self.distance_matrix,
            self.image_manager
        )
        
        # Set callback cho map click
        self.map_renderer.on_location_click = self.handle_map_click
        
        # Load hình ảnh
        self.image_manager.load_all_images(
            self.location_data.get_all_locations()
        )
        
        # Hiển thị danh sách ban đầu
        self.ui.create_location_list(self.selected_locations, 
                                     self.start_location,
                                     self.mandatory_locations)
    
    def _setup_callbacks(self):
        """Thiết lập các callback cho UI"""
        self.ui.on_location_toggle = self.toggle_location
        self.ui.on_district_change_callback = self.on_district_change
        self.ui.on_find_path = self.find_path
        self.ui.on_reset = self.reset_selection
    
    def handle_map_click(self, loc_id):
        # Chỉ cho phép click vào điểm đã được chọn trong list
        if loc_id not in self.selected_locations:
            return
        
        # TRƯỜNG HỢP 1: Chưa có điểm bắt đầu
        if self.start_location is None:
            self.start_location = loc_id
            # Tự động thêm vào danh sách bắt buộc
            if loc_id not in self.mandatory_locations:
                self.mandatory_locations.append(loc_id)
            
            loc_name = self.location_data.get_location(loc_id)["name"]
        # TRƯỜNG HỢP 2: Click vào điểm bắt đầu lần nữa (bỏ chọn)
        elif loc_id == self.start_location:
            self.start_location = None
            if loc_id in self.mandatory_locations:
                self.mandatory_locations.remove(loc_id)
        # TRƯỜNG HỢP 3: Click vào điểm khác (toggle bắt buộc)
        else:
            if loc_id in self.mandatory_locations:
                # Bỏ đánh dấu bắt buộc
                self.mandatory_locations.remove(loc_id)
                loc_name = self.location_data.get_location(loc_id)["name"]
            else:
                # Đánh dấu bắt buộc
                self.mandatory_locations.append(loc_id)
                loc_name = self.location_data.get_location(loc_id)["name"]
                
        # Reset path khi thay đổi
        self.path_result = None
        
        # Cập nhật UI
        self.ui.update_stats(self.selected_locations, self.start_location, 
                           self.mandatory_locations)
        self.map_renderer.draw_map(self.selected_locations, self.path_result, 
                                   self.start_location, self.mandatory_locations)
        self.ui.create_location_list(self.selected_locations, 
                                     self.start_location,
                                     self.mandatory_locations)
    
    def toggle_location(self, loc_id):
        """Toggle chọn/bỏ chọn địa điểm từ danh sách"""
        if loc_id in self.selected_locations:
            self.selected_locations.remove(loc_id)
            
            # Nếu bỏ chọn điểm đang là start, reset start
            if loc_id == self.start_location:
                self.start_location = None
            
            # Nếu bỏ chọn điểm bắt buộc, xóa khỏi mandatory
            if loc_id in self.mandatory_locations:
                self.mandatory_locations.remove(loc_id)
        else:
            self.selected_locations.append(loc_id)
        
        # Reset path khi thay đổi lựa chọn
        self.path_result = None
        
        # Cập nhật UI
        self.on_district_change()
        self.ui.update_stats(self.selected_locations, self.start_location,
                           self.mandatory_locations)
        self.map_renderer.draw_map(self.selected_locations, self.path_result, 
                                   self.start_location, self.mandatory_locations)
    
    def on_district_change(self):
        """Xử lý khi thay đổi bộ lọc quận"""
        self.ui.create_location_list(self.selected_locations, 
                                     self.start_location,
                                     self.mandatory_locations)
    
    def find_path(self, limit_km=None):
        """Tìm đường đi tối ưu"""
        # Kiểm tra điều kiện cơ bản
        if self.start_location is None:
            messagebox.showwarning("Thông báo", 
                                 "Vui lòng click chọn 1 điểm trên bản đồ để làm ĐIỂM BẮT ĐẦU!")
            return
        
        if len(self.selected_locations) < 1:
            messagebox.showwarning("Thông báo", 
                                 "Vui lòng chọn ít nhất 1 địa điểm!")
            return
        
        # Kiểm tra xem các điểm bắt buộc có khả thi không
        if limit_km and self.mandatory_locations:
            feasible, min_dist, best_order = self.path_finder.check_mandatory_feasibility(
                self.mandatory_locations, limit_km)
            
            if not feasible:
                # Các điểm bắt buộc không thể đi hết trong giới hạn
                loc_names = [self.location_data.get_location(loc)["name"] 
                            for loc in self.mandatory_locations]
                
                response = messagebox.askyesno(
                    "Vượt Giới Hạn Km",
                    f"⚠️ KHÔNG THỂ đi hết các điểm BẮT BUỘC trong {limit_km} km!\n\n"
                    f"Các điểm bắt buộc:\n" + "\n".join(f"  • {name}" for name in loc_names) + 
                    f"\n\nKhoảng cách tối thiểu: {min_dist:.2f} km\n"
                    f"Giới hạn của bạn: {limit_km} km\n\n"
                    f"Bạn có muốn bỏ bớt điểm bắt buộc không?",
                    icon='warning'
                )
                
                if response:
                    # Mở dialog chọn điểm cần bỏ
                    self._show_remove_mandatory_dialog()
                return
        
        # Tìm đường
        path, total_distance, exceeded_locations = self.path_finder.find_shortest_path_tsp(
            self.selected_locations, 
            start_location=self.start_location,
            mandatory_locations=self.mandatory_locations,
            limit_km=limit_km
        )
        
        if not path:
            messagebox.showinfo("Thông báo", 
                              "Không tìm được lộ trình phù hợp!\n"
                              "Hãy thử giảm số điểm hoặc tăng giới hạn km.")
            return
        
        # Kiểm tra xem có điểm optional bị bỏ qua không
        if exceeded_locations:
            loc_names = [self.location_data.get_location(loc)["name"] 
                        for loc in exceeded_locations]
            
            messagebox.showinfo(
                "Thông Báo",
                f"⚠️ Đã vượt {limit_km} km nếu đi hết các điểm!\n\n"
                f"Các điểm sau đã bị BỎ QUA:\n" + 
                "\n".join(f"  • {name}" for name in loc_names) +
                f"\n\nLộ trình chỉ đi qua các điểm BẮT BUỘC và\n"
                f"một số điểm tùy chọn trong giới hạn."
            )
        
        # Tìm các điểm trung gian
        visited_locations = [loc for loc in self.selected_locations 
                           if loc not in exceeded_locations]
        intermediate_locations = self.path_finder.find_intermediate_points(
            path, visited_locations)
        
        self.path_result = (path, total_distance, intermediate_locations, 
                          exceeded_locations)
        
        self.ui.display_result(self.path_result, self.start_location, 
                              self.mandatory_locations)
        self.map_renderer.draw_map(visited_locations, self.path_result, 
                                   self.start_location, self.mandatory_locations)
    
    def _show_remove_mandatory_dialog(self):
        """Hiển thị dialog để chọn điểm bắt buộc cần bỏ"""
        from tkinter import Toplevel, Checkbutton, BooleanVar
        
        dialog = Toplevel(self.root)
        dialog.title("Chọn Điểm Cần Bỏ")
        dialog.geometry("400x400")
        dialog.configure(bg="white")
        
        tk.Label(dialog, text="Chọn các điểm bắt buộc cần BỎ:",
                font=("Arial", 12, "bold"),
                bg="white").pack(pady=10)
        
        # Frame chứa checkboxes
        check_frame = tk.Frame(dialog, bg="white")
        check_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        vars_dict = {}
        for loc_id in self.mandatory_locations:
            if loc_id == self.start_location:
                continue  # Không cho bỏ điểm bắt đầu
            
            var = BooleanVar(value=False)
            vars_dict[loc_id] = var
            
            loc_name = self.location_data.get_location(loc_id)["name"]
            cb = Checkbutton(check_frame, text=loc_name, variable=var,
                           font=("Arial", 10), bg="white")
            cb.pack(anchor="w", pady=2)
        
        # Buttons
        def on_confirm():
            removed = [loc_id for loc_id, var in vars_dict.items() if var.get()]
            
            if not removed:
                messagebox.showwarning("Cảnh báo", "Bạn chưa chọn điểm nào để bỏ!")
                return
            
            for loc_id in removed:
                self.mandatory_locations.remove(loc_id)
            
            dialog.destroy()
            
            # Cập nhật UI
            self.ui.update_stats(self.selected_locations, self.start_location,
                               self.mandatory_locations)
            self.map_renderer.draw_map(self.selected_locations, self.path_result, 
                                       self.start_location, self.mandatory_locations)
            self.ui.create_location_list(self.selected_locations, 
                                         self.start_location,
                                         self.mandatory_locations)
            
            messagebox.showinfo("Thành Công", 
                              f"Đã bỏ {len(removed)} điểm bắt buộc!\n"
                              f"Hãy thử tìm đường lại.")
        
        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Xác Nhận", command=on_confirm,
                 bg="#10b981", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Hủy", command=dialog.destroy,
                 bg="#6b7280", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
    
    def reset_selection(self):
        """Đặt lại toàn bộ lựa chọn"""
        if (not self.selected_locations and not self.path_result and 
            not self.start_location and not self.mandatory_locations):
            messagebox.showinfo("Thông Báo", "Không có gì để đặt lại!")
            return
        
        # Reset state
        self.selected_locations = []
        self.start_location = None
        self.mandatory_locations = []
        self.path_result = None
        
        # Cập nhật UI
        self.on_district_change()
        self.ui.update_stats(self.selected_locations, self.start_location,
                           self.mandatory_locations)
        self.map_renderer.draw_map(self.selected_locations, self.path_result,
                                   self.start_location, self.mandatory_locations)
        self.ui.reset_result_display()


def main():
    """Entry point của ứng dụng"""
    root = tk.Tk()
    app = HanoiTourismApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
