"""
Module xử lý và quản lý hình ảnh
"""
from PIL import Image, ImageTk, ImageDraw
import os


class ImageManager:
    """Class quản lý việc load và xử lý hình ảnh"""
    
    def __init__(self):
        self.images_cache = {}  # Cache để lưu hình ảnh
    
    def load_all_images(self, locations):
        """
        Load tất cả hình ảnh cho các địa điểm
        
        Args:
            locations: Dict chứa thông tin các địa điểm
        """
        for loc_id, data in locations.items():
            image_path = data.get("image")
            
            # Nếu file ảnh tồn tại, load nó
            if image_path and os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    
                    # Resize cho thumbnail (80x60)
                    img_thumb = img.resize((80, 60), Image.Resampling.LANCZOS)
                    self.images_cache[f"{loc_id}_thumb"] = ImageTk.PhotoImage(img_thumb)
                    
                    # Resize cho map (80x80) và tạo hình tròn
                    img_map = self.create_round_image(img, 80)
                    self.images_cache[f"{loc_id}_map"] = ImageTk.PhotoImage(img_map)
                    
                except Exception as e:
                    print(f"Lỗi load ảnh {image_path}: {e}")
                    self.create_placeholder(loc_id)
            else:
                # Tạo placeholder nếu không có ảnh
                self.create_placeholder(loc_id)
    
    def create_round_image(self, img, size):
        """
        Tạo hình ảnh tròn từ hình gốc
        
        Args:
            img: PIL Image object
            size: Kích thước (width = height)
            
        Returns:
            PIL Image: Ảnh đã bo tròn
        """
        # Resize
        img_resized = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Tạo mask hình tròn
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # Apply mask
        img_resized.putalpha(mask)
        
        return img_resized
    
    def create_placeholder(self, loc_id):
        """
        Tạo ảnh placeholder khi không load được ảnh thật
        
        Args:
            loc_id: ID của địa điểm
        """
        # Tạo ảnh màu xám cho thumbnail
        img_thumb = Image.new('RGB', (80, 60), color='#94a3b8')
        self.images_cache[f"{loc_id}_thumb"] = ImageTk.PhotoImage(img_thumb)
        
        # Tạo ảnh màu xám tròn cho map
        img_map = Image.new('RGB', (80, 80), color='#64748b')
        
        # Bo tròn
        mask = Image.new('L', (80, 80), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 80, 80), fill=255)
        img_map.putalpha(mask)
        
        self.images_cache[f"{loc_id}_map"] = ImageTk.PhotoImage(img_map)
    
    def get_image(self, key):
        """
        Lấy hình ảnh từ cache
        
        Args:
            key: Key của ảnh trong cache
            
        Returns:
            ImageTk.PhotoImage hoặc None
        """
        return self.images_cache.get(key)
    
    def clear_cache(self):
        """Xóa cache hình ảnh"""
        self.images_cache.clear()
