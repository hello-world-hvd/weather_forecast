# utils.py
import json
import os
from datetime import *
import pytz
from timezonefinder import TimezoneFinder
import requests
from requests.structures import CaseInsensitiveDict

def load_location(address):
    api_key = "f5ffe47cbd3740f0b85f5721a16886aa"
    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey={api_key}"
    
    # Headers của yêu cầu
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    
    # Gửi yêu cầu GET đến API
    response = requests.get(url, headers=headers)
    
    # Kiểm tra mã trạng thái
    if response.status_code == 200:
        data = response.json()
        
        # Kiểm tra xem có dữ liệu nào trong 'features' không
        if data["features"]:
            # Trích xuất latitude và longitude từ 'geometry' trong phản hồi
            latitude = data["features"][0]["geometry"]["coordinates"][1]
            longitude = data["features"][0]["geometry"]["coordinates"][0]
            loc = type('Location', (object,), {
                'latitude': latitude,
                'longitude': longitude
            })
            return loc
        else:
            return "Không tìm thấy tọa độ cho địa chỉ này."
    else:
        return f"Lỗi khi gửi yêu cầu: {response.status_code}"

def get_current_time(location, time_update_id=None):
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    return local_time.strftime("%I:%M %p")


