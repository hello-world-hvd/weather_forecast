import os
import json
import geocoder
from datetime import *
import pytz
from timezonefinder import TimezoneFinder

def save_location(city, loc):
    if(os.path.exists('locations_data.json')):
        with open('location_data.json', 'r') as f:
            locations = json.load(f)
    else:
        locations = {}

    locations[city] = {
        'latitude': loc.latitude,
        'longitude': loc.longitude
    }

    with open('location_data.json', 'w') as f:
        json.dump(locations, f)

def get_current_time(location, time_update_id=None):
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    return local_time.strftime("%I:%M %p")

