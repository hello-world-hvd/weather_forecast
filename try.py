from PIL import Image

def convert_to_white_icon(input_path, output_path):
    # Mở ảnh
    img = Image.open(input_path)
    
    # Chuyển sang chế độ RGBA nếu chưa phải
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Lấy dữ liệu pixel
    data = img.getdata()
    
    # Tạo dữ liệu mới với pixels màu trắng
    new_data = []
    for item in data:
        # Nếu pixel không trong suốt (alpha > 0)
        if item[3] > 0:
            # Thay thế bằng màu đỏ (255, 0, 0) và giữ nguyên độ trong suốt
            new_data.append((255, 0, 0, item[3]))
        else:
            # Giữ nguyên các pixel trong suốt
            new_data.append(item)
    
    # Cập nhật dữ liệu pixel mới
    img.putdata(new_data)
    
    # Lưu ảnh
    img.save(output_path, 'PNG')

# Sử dụng hàm
convert_to_white_icon('Images/heart.png', 'Images/heart_red.png')