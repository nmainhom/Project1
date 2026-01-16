"""
Module quản lý dữ liệu địa điểm và khoảng cách
"""


class LocationData:
    """Class quản lý thông tin các địa điểm du lịch"""
    
    def __init__(self):
        self.locations = {
            # QUẬN HOÀN KIẾM
            "hk1": {
                "name": "Hồ Hoàn Kiếm",
                "district": "Hoàn Kiếm",
                "description": "Biểu tượng của Hà Nội ",
                "x": 300, "y": 250,
                "image": "images/pic1.jpg"
            },
            "hk2": {
                "name": "Nhà Thờ Lớn",
                "district": "Hoàn Kiếm",
                "description": "Kiến trúc Gothic độc đáo",
                "x": 150, "y": 180,
                "image": "images/pic2.jpg"
            },
            "hk3": {
                "name": "Phố Tạ Hiện",
                "district": "Hoàn Kiếm",
                "description": "Phố đêm không ngủ giữa lòng Hà Nội",
                "x": 250, "y": 50,
                "image": "images/pic3.jpg"
            },
            "hk4": {
                "name": "Chợ Đồng Xuân",
                "district": "Hoàn Kiếm",
                "description": "Khu chợ lớn và lịch sử nằm ở trung tâm phố cổ Hà Nội",
                "x": 400, "y": 100,
                "image": "images/pic4.jpg"
            },
            
            # QUẬN BA ĐÌNH
            "bd1": {
                "name": "Lăng Chủ Tịch Hồ Chí Minh",
                "district": "Ba Đình",
                "description": "Nơi gìn giữ thi hài Chủ tịch Hồ Chí Minh.",
                "x": 150, "y": 420,
                "image": "images/pic5.jpg"
            },
            "bd2": {
                "name": "Văn Miếu Quốc Tử Giám",
                "district": "Ba Đình",
                "description": "Trường đại học đầu tiên tại Việt Nam",
                "x": 100, "y": 300,
                "image": "images/pic7.jpg"
            },
            "bd3": {
                "name": "Hoàng Thành Thăng Long",
                "district": "Ba Đình",
                "description": "Quần thể di tích gắn liền với lịch sử kinh thành Thăng Long - Đông Kinh",
                "x": 250, "y": 480,
                "image": "images/pic8.jpg"
            },
            "bd4": {
                "name": "Cột cờ Hà Nội",
                "district": "Ba Đình",
                "description": "“chứng nhân lịch sử” của Thủ đô trong thời kỳ kháng chiến chống Pháp oanh liệt.",
                "x": 380, "y": 380,
                "image": "images/pic16.jpg"
            },
            
            # QUẬN TÂY HỒ
            "th1": {
                "name": "Hồ Tây",
                "district": "Tây Hồ",
                "description": "Hồ nước ngọt lớn nhất Hà Nội",
                "x": 600, "y": 100,
                "image": "images/pic9.jpg"
            },
            "th2": {
                "name": "Chùa Trấn Quốc",
                "district": "Tây Hồ",
                "description": "Ngôi chùa cổ nhất Hà Nội",
                "x": 520, "y": 200,
                "image": "images/pic10.jpg"
            },
            "th3": {
                "name": "Phủ Tây Hồ",
                "district": "Tây Hồ",
                "description": "Nơi thờ Thánh Mẫu Liễu Hạnh",
                "x": 600, "y": 300,
                "image": "images/pic11.jpg"
            },
            
            # QUẬN ĐỐNG ĐA
            "dd1": {
                "name": "Thành Cổ Đống Đa",
                "district": "Đống Đa",
                "description": "Di tích chiến thắng Ngọc Hồi",
                "x": 700, "y": 400,
                "image": "images/pic12.jpg"
            },
            "dd2": {
                "name": "Lotte Center",
                "district": "Đống Đa",
                "description": "Tòa nhà cao nhất Hà Nội",
                "x": 600, "y": 450,
                "image": "images/pic13.jpg"
            },
            
            # QUẬN HAI BÀ TRƯNG
            "hbt1": {
                "name": "Đền Hai Bà Trưng",
                "district": "Hai Bà Trưng",
                "description": "Tôn vinh hai nữ anh hùng",
                "x": 800, "y": 100,
                "image": "images/pic14.jpg"
            },
            "hbt2": {
                "name": "Công Viên Thống Nhất",
                "district": "Hai Bà Trưng",
                "description": "Công viên lớn giữa lòng Hà Nội",
                "x": 800, "y": 250,
                "image": "images/pic15.jpg"
            }
        }
    
    def get_location(self, loc_id):
        """Lấy thông tin một địa điểm"""
        return self.locations.get(loc_id)
    
    def get_all_locations(self):
        """Lấy tất cả địa điểm"""
        return self.locations
    
    def get_locations_by_district(self, district):
        """Lấy các địa điểm theo quận"""
        if district == "Tất cả":
            return self.locations
        return {
            loc_id: loc_data
            for loc_id, loc_data in self.locations.items()
            if loc_data["district"] == district
        }
    
    def get_districts(self):
        """Lấy danh sách các quận"""
        districts = set()
        for loc_data in self.locations.values():
            districts.add(loc_data["district"])
        return ["Tất cả"] + sorted(list(districts))


class DistanceMatrix:
    """Class quản lý ma trận khoảng cách giữa các địa điểm"""
    
    def __init__(self):
        self.distances = {
            # Hoàn Kiếm nội bộ
            ("hk1", "hk2"): 0.8,
            ("hk1", "hk3"): 0.8,
            ("hk1", "hk4"): 1.2,
            ("hk2", "hk3"): 1.0,
            ("hk2", "hk4"): 1.3,
            ("hk3", "hk4"): 0.5,
            
            # Hoàn Kiếm - Ba Đình
            ("hk1", "bd1"): 2.9,
            ("hk1", "bd2"): 2.2,
            ("hk1", "bd3"): 2.2,
            ("hk2", "bd1"): 2.5,
            ("hk2", "bd2"): 1.8,
            ("hk2", "bd3"): 1.8,
            ("hk3", "bd1"): 3.0,
            ("hk3", "bd2"): 2.3,
            ("hk3", "bd3"): 2.3,
            ("hk4", "bd1"): 3.1,
            ("hk4", "bd2"): 2.5,
            ("hk4", "bd3"): 2.3,
            
            # Ba Đình nội bộ
            ("bd1", "bd2"): 1.8,
            ("bd1", "bd3"): 1.2,
            ("bd2", "bd3"): 1.4,
            
            # Tây Hồ nội bộ
            ("th1", "th2"): 1.0,
            ("th1", "th3"): 1.5,
            ("th2", "th3"): 0.8,
            
            # Hoàn Kiếm - Tây Hồ
            ("hk1", "th1"): 6.4,
            ("hk1", "th2"): 5.9,
            ("hk2", "th1"): 6.5,
            ("hk2", "th2"): 3.5,
            ("hk2", "th3"): 6.3,
            ("hk3", "th1"): 5.9,
            ("hk3", "th2"): 3.0,
            ("hk3", "th3"): 5.6,
            ("hk4", "th1"): 4.6,
            ("hk4", "th2"): 2.6,
            ("hk4", "th3"): 5.2,
            
            # Ba Đình - Tây Hồ
            ("bd1", "th1"): 6.0,
            ("bd1", "th2"): 2.2,
            ("bd1", "th3"): 5.8,
            ("bd2", "th1"): 6.6,
            ("bd2", "th2"): 2.8,
            ("bd2", "th3"): 6.8,
            ("bd3", "th1"): 6.1,
            ("bd3", "th2"): 2.3,
            ("bd3", "th3"): 6.0,
            
            # Đống Đa nội bộ
            ("dd1", "dd2"): 2.0,
            
            # Ba Đình - Đống Đa
            ("bd1", "dd1"): 2.5,
            ("bd2", "dd1"): 2.2,
            ("bd2", "dd2"): 2.5,
            ("bd3", "dd1"): 3.2,
            ("bd3", "dd2"): 3.5,
            ("bd4", "dd1"): 2.0,
            ("bd4", "dd2"): 2.8,
            
            # Hoàn Kiếm - Đống Đa
            ("hk1", "dd1"): 4.5,
            ("hk1", "dd2"): 4.2,
            ("hk2", "dd1"): 4.8,
            ("hk3", "dd2"): 5.0,
            ("hk4", "dd1"): 4.7,
            
            # Tây Hồ - Đống Đa
            ("th1", "dd1"): 6.0,
            ("th1", "dd2"): 5.8,
            ("th2", "dd1"): 6.5,
            ("th2", "dd2"): 6.2,
            ("th3", "dd1"): 6.8,
            ("th3", "dd2"): 6.5,
            
            # Hai Bà Trưng nội bộ
            ("hbt1", "hbt2"): 1.5,
            
            # Hoàn Kiếm - Hai Bà Trưng
            ("hk1", "hbt1"): 3.5,
            ("hk1", "hbt2"): 4.0,
            ("hk3", "hbt1"): 4.2,
            ("hk4", "hbt1"): 3.8,
            ("hk4", "hbt2"): 4.3,
            
            # Ba Đình - Hai Bà Trưng
            ("bd1", "hbt1"): 5.5,
            ("bd2", "hbt1"): 6.0,
            ("bd3", "hbt1"): 6.2,
            ("bd4", "hbt1"): 5.8,
            ("bd4", "hbt2"): 6.5,
            
            # Tây Hồ - Hai Bà Trưng
            ("th1", "hbt1"): 7.0,
            ("th2", "hbt1"): 7.5,
            ("th3", "hbt1"): 7.8,
            ("th3", "hbt2"): 8.0,
            
            # Đống Đa - Hai Bà Trưng
            ("dd1", "hbt1"): 3.5,
            ("dd1", "hbt2"): 4.0,
            ("dd2", "hbt1"): 3.2,
            ("dd2", "hbt2"): 3.8,
        }
    
    def get_distance(self, loc1, loc2):
        """Lấy khoảng cách giữa 2 địa điểm"""
        edge = tuple(sorted([loc1, loc2]))
        return self.distances.get(edge)
    
    def is_connected(self, loc1, loc2):
        """Kiểm tra 2 địa điểm có kết nối trực tiếp không"""
        edge = tuple(sorted([loc1, loc2]))
        return edge in self.distances
    
    def get_all_distances(self):
        """Lấy toàn bộ ma trận khoảng cách"""
        return self.distances
