import os
import json
import geocoder
from datetime import *
import pytz
from timezonefinder import TimezoneFinder

def save_location(city, loc):
    # Kiểm tra nếu file 'location_data.json' đã tồn tại
    if os.path.exists('location_data.json'):
        with open('location_data.json', 'r') as f:
            # Đọc dữ liệu từ file JSON
            locations = json.load(f)
    else:
        # Nếu file chưa tồn tại, khởi tạo danh sách rỗng
        locations = []

    new_location = {
        'name': city,
        'latitude': loc.latitude,
        'longitude': loc.longitude
    }
    locations.append(new_location)

    with open('location_data.json', 'w') as f:
        json.dump(locations, f, indent=4)
        
def remove_location(location, locations_list):
    for loc in locations_list:
        if loc['latitude'] == location.latitude and loc['longitude'] == location.longitude:
            locations_list.remove(loc)
            return
    return

def save_location_list(locations):
    with open('location_data.json', 'w') as file:
        json.dump(locations, file, indent=4)

def load_location_list():
    with open('location_data.json', 'r') as file:
        return json.load(file)

def is_location_in_list(location, locations_list):
    for loc in locations_list:
        if loc['latitude'] == location.latitude and loc['longitude'] == location.longitude:
            return True
    return False

def get_current_time(location, time_update_id=None):
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    return local_time.strftime("%I:%M %p")

