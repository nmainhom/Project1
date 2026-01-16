"""
Module chứa các thuật toán tìm đường tối ưu
"""
from itertools import permutations


class PathFinder:
    """Class xử lý các thuật toán tìm đường"""
    
    def __init__(self, location_data, distance_matrix):
        """
        Khởi tạo PathFinder
        
        Args:
            location_data: Instance của LocationData
            distance_matrix: Instance của DistanceMatrix
        """
        self.location_data = location_data
        self.distance_matrix = distance_matrix
    
    def build_graph(self):
        """Xây dựng đồ thị từ TẤT CẢ các địa điểm"""
        locations = self.location_data.get_all_locations()
        graph = {loc_id: [] for loc_id in locations.keys()}
        
        distances = self.distance_matrix.get_all_distances()
        for (loc1, loc2), distance in distances.items():
            graph[loc1].append((loc2, distance))
            graph[loc2].append((loc1, distance))
        
        return graph
    
    def dijkstra(self, graph, start, end):
        """
        Thuật toán Dijkstra tìm đường đi ngắn nhất
        
        Args:
            graph: Đồ thị dạng adjacency list
            start: Điểm bắt đầu
            end: Điểm kết thúc
            
        Returns:
            tuple: (path, distance) - đường đi và khoảng cách
        """
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        previous = {node: None for node in graph}
        unvisited = set(graph.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda node: distances[node])
            
            if current == end or distances[current] == float('infinity'):
                break
            
            unvisited.remove(current)
            
            for neighbor, weight in graph[current]:
                distance = distances[current] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
        
        if distances[end] == float('infinity'):
            return [], None
        
        # Xây dựng đường đi
        path = []
        current = end
        while current:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        return path, distances[end]
    
    def find_shortest_path_tsp(self, selected_locations, start_location=None, 
                               mandatory_locations=None, limit_km=None):
        """
        Giải bài toán TSP với điểm bắt buộc và giới hạn km
        
        Args:
            selected_locations: Danh sách các địa điểm đã chọn (bao gồm cả optional)
            start_location: Điểm bắt đầu cố định
            mandatory_locations: Danh sách điểm BẮT BUỘC phải đi qua
            limit_km: Giới hạn km (None = không giới hạn)
            
        Returns:
            tuple: (path, total_distance, exceeded_locations) 
                   - exceeded_locations: danh sách điểm bị bỏ qua do vượt giới hạn km
        """
        if not selected_locations or len(selected_locations) < 1:
            return [], 0, []
        
        # Build graph
        graph = self.build_graph()
        
        # Xác định điểm bắt buộc
        if mandatory_locations is None:
            mandatory_locations = []
        
        # Nếu có start_location, thêm vào danh sách bắt buộc
        if start_location:
            if start_location not in mandatory_locations:
                mandatory_locations = [start_location] + mandatory_locations
        
        # Lấy các điểm tùy chọn (optional)
        optional_locations = [loc for loc in selected_locations 
                             if loc not in mandatory_locations]
        
        best_distance = float('infinity')
        best_path = []
        best_visited = []
        exceeded_locations = []
        
        # Thử các tổ hợp khác nhau của điểm optional
        # Từ đầy đủ nhất đến ít nhất
        for num_optional in range(len(optional_locations), -1, -1):
            from itertools import combinations
            
            # Thử tất cả tổ hợp num_optional điểm từ optional_locations
            for optional_combo in combinations(optional_locations, num_optional):
                # Tạo danh sách điểm cần đi qua
                locations_to_visit = list(mandatory_locations) + list(optional_combo)
                
                # Nếu có start_location, tách riêng
                if start_location and start_location in locations_to_visit:
                    other_locs = [loc for loc in locations_to_visit if loc != start_location]
                    
                    # Thử tất cả hoán vị của các điểm còn lại
                    for perm in permutations(other_locs):
                        full_perm = (start_location,) + perm
                        
                        full_path = []
                        total_distance = 0
                        valid = True
                        
                        for i in range(len(full_perm) - 1):
                            segment_path, segment_dist = self.dijkstra(
                                graph, full_perm[i], full_perm[i + 1])
                            
                            if not segment_path:
                                valid = False
                                break
                            
                            if i == 0:
                                full_path.extend(segment_path)
                            else:
                                full_path.extend(segment_path[1:])
                            
                            total_distance += segment_dist
                            
                            # Kiểm tra giới hạn km
                            if limit_km and total_distance > limit_km:
                                valid = False
                                break
                        
                        if valid:
                            if total_distance < best_distance:
                                best_distance = total_distance
                                best_path = full_path
                                best_visited = list(locations_to_visit)
                else:
                    # Không có start_location
                    for perm in permutations(locations_to_visit):
                        full_path = []
                        total_distance = 0
                        valid = True
                        
                        for i in range(len(perm) - 1):
                            segment_path, segment_dist = self.dijkstra(
                                graph, perm[i], perm[i + 1])
                            
                            if not segment_path:
                                valid = False
                                break
                            
                            if i == 0:
                                full_path.extend(segment_path)
                            else:
                                full_path.extend(segment_path[1:])
                            
                            total_distance += segment_dist
                            
                            # Kiểm tra giới hạn km
                            if limit_km and total_distance > limit_km:
                                valid = False
                                break
                        
                        if valid:
                            if total_distance < best_distance:
                                best_distance = total_distance
                                best_path = full_path
                                best_visited = list(locations_to_visit)
            
            # Nếu đã tìm được đường đi hợp lệ, dừng
            if best_path:
                break
        
        # Tính toán các điểm bị bỏ qua
        if best_visited:
            exceeded_locations = [loc for loc in selected_locations 
                                 if loc not in best_visited]
        else:
            # Nếu không tìm được đường nào, tất cả optional đều bị bỏ
            exceeded_locations = optional_locations
        
        return best_path, best_distance, exceeded_locations
    
    def find_intermediate_points(self, path, selected_locations):
        """
        Tìm các điểm trung gian trên đường đi
        
        Args:
            path: Đường đi đầy đủ
            selected_locations: Các điểm được chọn
            
        Returns:
            list: Danh sách các điểm trung gian
        """
        intermediate = []
        
        for loc_id in path:
            if loc_id not in selected_locations:
                intermediate.append(loc_id)
        
        return intermediate
    
    def calculate_total_distance(self, path):
        """
        Tính tổng quãng đường của một path
        
        Args:
            path: Đường đi
            
        Returns:
            float: Tổng quãng đường (km)
        """
        total = 0
        for i in range(len(path) - 1):
            dist = self.distance_matrix.get_distance(path[i], path[i + 1])
            if dist:
                total += dist
        return total
    
    def check_mandatory_feasibility(self, mandatory_locations, limit_km):
        """
        Kiểm tra xem các điểm bắt buộc có thể đi hết trong giới hạn km không
        
        Args:
            mandatory_locations: Danh sách điểm bắt buộc
            limit_km: Giới hạn km
            
        Returns:
            tuple: (feasible, min_distance, best_order)
        """
        if not mandatory_locations or len(mandatory_locations) < 2:
            return True, 0, mandatory_locations
        
        graph = self.build_graph()
        best_distance = float('infinity')
        best_order = []
        
        # Thử tất cả hoán vị
        for perm in permutations(mandatory_locations):
            total_distance = 0
            valid = True
            
            for i in range(len(perm) - 1):
                _, segment_dist = self.dijkstra(graph, perm[i], perm[i + 1])
                
                if segment_dist is None:
                    valid = False
                    break
                
                total_distance += segment_dist
            
            if valid and total_distance < best_distance:
                best_distance = total_distance
                best_order = list(perm)
        
        feasible = best_distance <= limit_km if limit_km else True
        
        return feasible, best_distance, best_order