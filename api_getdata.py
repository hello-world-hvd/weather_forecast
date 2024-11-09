import requests
import geocoder
from requests.structures import CaseInsensitiveDict

api_key_location= "f5ffe47cbd3740f0b85f5721a16886aa"
api_key_data = "a40a08819e2ca4455e9badc3a50026b6"

def get_current_location():
    cur_loc = geocoder.ip('me')
    return cur_loc

def load_location(address):
    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey={api_key_location}"
    
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

def reverse_location(latitude, longitude):
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&apiKey={api_key_location}"
    
    response = requests.get(url)
    data = response.json()
    
    if 'features' in data and len(data['features']) > 0:
        properties = data['features'][0]['properties']
        city = properties.get('city', 'Không rõ')
        country = properties.get('country', 'Không rõ')
        return city, country
    else:
        return "Không tìm thấy địa chỉ", "Không tìm thấy quốc gia"

def get_json_data(location):
    api = f"https://api.openweathermap.org/data/2.8/onecall?lat={location.latitude}&lon={location.longitude}&units=metric&exclude=hourly&appid={api_key_data}"
    json_data=requests.get(api).json()
    return json_data

def get_aqi_color(aqi):
    if aqi <= 50: return "#00e400"      # Good
    elif aqi <= 100: return "#ffff00"    # Moderate
    elif aqi <= 150: return "#ff7e00"    # Unhealthy for Sensitive Groups
    elif aqi <= 200: return "#ff0000"    # Unhealthy
    elif aqi <= 300: return "#8f3f97"    # Very Unhealthy
    else: return "#7e0023"               # Hazardous

def get_aqi_text(aqi):
    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 150: return "Unhealthy for Sensitive Groups"
    elif aqi <= 200: return "Unhealthy"
    elif aqi <= 300: return "Very Unhealthy"
    else: return "Hazardous"

def get_aqi(location):
    try:
        # Replace with your actual AQI API endpoint
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={location.latitude}&lon={location.longitude}&appid={api_key_data}"
        aqi_response = requests.get(aqi_url)
        aqi_data = aqi_response.json()
        aqi = aqi_data['list'][0]['main']['aqi'] * 50  # Convert to AQI scale
        aqi_value=f"{aqi}"
        aqi_status=[
            f"({get_aqi_text(aqi)})",
            get_aqi_color(aqi)
        ]
        return aqi_value, aqi_status
    except Exception as e:
        print(f"Error fetching AQI data: {e}")
        return aqi

