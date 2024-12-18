import json
import os
from pkgutil import get_data
from tkinter import*
import tkinter as tk
from turtle import update
from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from numpy import resize
from timezonefinder import TimezoneFinder
from datetime import*
import requests
import pytz
from PIL import Image, ImageTk
from app import get_current_time
import customtkinter
from api_getdata import get_aqi, get_json_data2
from datetime import datetime, timedelta
from pkgutil import get_data

class WeatherDetail:
    def __init__(self, root, data, city, time_update_id, location):
        self.root = root
        self.data = data
        self.city = city
        self.location = location
        self.time_update_id = time_update_id
        
        # Configure root window
        # self.root.configure(bg="#F0F2F6")
        
        self.create_detail_interface()
        self.update_clock()
        self.getData()
        self.getdata = get_json_data2(self.location)

    def switch_to_main_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from weather import WeatherApp
        Main = WeatherApp(self.root, self.data, self.time_update_id, self.city, self.location)
        Main.create_main_interface(self.city, self.data, self.location)
        
    def show_new_weather_details(self):
        """Display hourly weather details when user clicks for more information."""
        for widget in self.root.winfo_children():
            widget.pack_forget()

        new_frame = Frame(self.root, bg="#57adff")
        new_frame.pack(fill="both", expand=True)

        img = Image.open("Images/back vector.png")
        back_resize = img.resize((40, 40))
        back = ImageTk.PhotoImage(back_resize)
        back_button = Button(
            new_frame, image=back, borderwidth=0, cursor="hand2", bg="#57adff",
            activebackground="#57adff", command=self.switch_to_weather_interface
        )
        back_button.image = back
        back_button.place(x=20, y=20)

        title_label = Label(new_frame, text="Dự báo theo giờ", font=("Helvetica", 24, "bold"), bg="#57adff", fg="white")
        title_label.pack(pady=20)

        hourly_frame = Frame(new_frame, bg="#57adff")
        hourly_frame.pack(pady=20)

        # Get current time in local timezone
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=self.location.longitude, lat=self.location.latitude)

        home = pytz.timezone(result)
        current_time = datetime.now(home).replace(minute=0, second=0, microsecond=0)

        # Configure grid to make sure columns and rows are responsive
        columns = 6  # 6 columns per row
        rows = 2  # Display in 2 rows

        # Create grid system
        for i in range(columns):
            hourly_frame.grid_columnconfigure(i, weight=1, uniform="equal")  # Ensure equal column widths
        for i in range(rows):
            hourly_frame.grid_rowconfigure(i, weight=1, uniform="equal")  # Ensure equal row heights

        hour_counter = 0  # Start from the first cell

        for i in range(len(self.getdata['hourly'])):
            hour_info = self.getdata['hourly'][i]
            temp_celsius = round(hour_info['temp'])
            weather_desc = hour_info['weather'][0]['description'].capitalize()
            icon_code = hour_info['weather'][0]['icon']

            timestamp = hour_info['dt']
            hour_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
            local_time = hour_time.astimezone(home)

            if local_time > current_time:
                formatted_time = local_time.strftime("%I %p")

                # Calculate row and column
                row = hour_counter // columns
                col = hour_counter % columns

                # Create a frame for the weather information
                single_hour_frame = Frame(hourly_frame, bg="#57adff", bd=2, relief="solid")  # Add border to frame
                single_hour_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

                # Icon
                icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
                try:
                    response = requests.get(icon_url, stream=True)
                    if response.status_code == 200:
                        icon_img = Image.open(response.raw).resize((50, 50))  # Resize icon
                        weather_icon = ImageTk.PhotoImage(icon_img)
                    else:
                        weather_icon = None
                except requests.exceptions.RequestException:
                    weather_icon = None

                if weather_icon:
                    icon_label = Label(single_hour_frame, image=weather_icon, bg="#57adff")
                    icon_label.image = weather_icon
                    icon_label.pack(pady=(5, 0))  # Icon at top
                else:
                    icon_label = Label(single_hour_frame, text="❓", font=("Helvetica", 16), bg="#57adff", fg="white")
                    icon_label.pack(pady=(5, 0))  # If no icon

                # Text details
                hour_label = Label(
                    single_hour_frame,
                    text=f"{formatted_time}\n{temp_celsius}°C\n{weather_desc}\nHumidity: {hour_info['humidity']}%\nWind: {hour_info['wind_speed']} m/s",
                    font=("Helvetica", 11), bg="#57adff", fg="white", justify="center"
                )
                hour_label.pack(pady=(5, 0))  # Text at the bottom

                hour_counter += 1  # Move to next cell

                # Stop after displaying 12 items
                if hour_counter == 12:
                    break

    def switch_to_weather_interface(self):
        # Xóa toàn bộ giao diện hiện tại
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Quay lại giao diện 2 (giao diện thời tiết chi tiết)
        self.create_detail_interface()  # Gọi lại phương thức tạo giao diện thời tiết chi tiết
        self.getData() 
    

    def update_clock(self):
        self.current_time = get_current_time(self.location)
        self.clock.config(text=self.current_time)
        self.clock.after(1000, self.update_clock)

    def getData(self):
        # Temperature data
        self.t = self.data['current']['temp']
        self.tempDay = self.data['daily'][0]['temp']['day']
        self.tempNight = self.data['daily'][0]['temp']['night']
        self.temp.config(text=f"{self.t}°C")
        self.tempDN.config(text=f"Day {self.tempDay}°C  •  Night {self.tempNight}°C")

        # Additional weather data
        self.pressure = self.data['current']['pressure']
        self.humidity = self.data['current']['humidity']
        self.clouds = self.data['current']['clouds']
        self.uvi = self.data['current']['uvi']
        self.visibility = self.data['current']['visibility']
        self.wind_speed = self.data['current']['wind_speed']

        # Update info cards
        self.pressure_value.config(text=f"{self.pressure}")
        self.humidity_value.config(text=f"{self.humidity}")
        self.clouds_value.config(text=f"{self.clouds}")
        self.uvi_value.config(text=f"{self.uvi}")
        self.visibility_value.config(text=f"{self.visibility/1000:.1f}")
        self.wind_value.config(text=f"{self.wind_speed}")

    def create_info_card(self, parent, title, unit, icon_path):
        card = customtkinter.CTkFrame(
            parent, 
            corner_radius=10,
            fg_color="#282829",
            border_width=1,  
            border_color="white",
            width=200, height=130
        )
        card.pack_propagate(False)
        
        try:
            icon = Image.open(icon_path)
            icon = icon.resize((24, 24))
            icon_photo = ImageTk.PhotoImage(icon)
            icon_label = Label(card, image=icon_photo, bg="#282829")
            icon_label.image = icon_photo
            icon_label.pack(pady=(5,5))
        except:
            pass

        title_label = Label(card, text=title, font=("Helvetica", 12), bg="#282829", fg="#f0f2f6")
        title_label.pack()
        
        value_label = Label(card, text="", font=("Helvetica", 20, "bold"), bg="#282829", fg="white")
        value_label.pack()
        
        unit_label = Label(card, text=unit, font=("Helvetica", 10), bg="#282829", fg="#f0f2f6")
        unit_label.pack()
        
        return card, value_label

    def icon_current_weather(self, current_time):
        time_sunrise = self.data['current']['sunrise']
        time_sunset = self.data['current']['sunset']
        sunrise = datetime.fromtimestamp(time_sunrise)
        sunset = datetime.fromtimestamp(time_sunset)
        current = datetime.strptime(current_time, "%I:%M %p")
        current = datetime.combine(datetime.now().date(), current.time())

        img_code = self.data['daily'][0]['weather'][0]['icon']
        icon_code = img_code[:-1]
        print("sunrise:", sunrise)
        print("sunset", sunset)
        print("current time:", current)
        
        if sunrise <= current <= sunset:
            return f"icon/{icon_code}d@2x.png"
        else:
            return f"icon/{icon_code}n@2x.png"        

    def create_detail_interface(self):
        ## Top bar
        top_frame = Frame(self.root, bg="#57adff", height=80)
        top_frame.pack(fill=X)

        
        # Home button
        img = Image.open("Images/home.png")
        home_resize = img.resize((40, 40))
        home = ImageTk.PhotoImage(home_resize)
        home_button = Button(
            top_frame,
            image=home,
            borderwidth=0,
            cursor="hand2",
            bg="#57adff",
            activebackground="#57adff",
            command=self.switch_to_main_interface
        )
        home_button.image = home
        home_button.place(x=900, y=20)

        # Clock
        self.clock = Label(
            self.root,
            font=("Helvetica", 30, 'bold'),
            fg="white",
            bg="#57adff"
        )
        self.clock.place(x=(self.root.winfo_width()-100) // 2, y=20)

        # Main content frame
        main_frame = Frame(self.root, bg="#212120")
        main_frame.pack(fill=BOTH, expand=True, padx=0)

        # Location and temperature section
        location_temp_frame = Frame(main_frame, bg="#212120")
        location_temp_frame.pack(fill=X, pady=(0,0))

        # Location
        loc_frame = Frame(location_temp_frame, bg="#282829", padx=10, pady=5, highlightbackground="white", highlightthickness=1)
        loc_frame.pack(side=LEFT, padx=(40, 10))

        img = Image.open("Images/location_white.png")
        loc_resize = img.resize((24, 24))
        self.locImage = ImageTk.PhotoImage(loc_resize)
        loc_label = Label(loc_frame, image=self.locImage, bg="#282829")
        loc_label.pack(side=LEFT)

        city_label = Label(
            loc_frame,
            text=self.city.upper(),
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg="#282829",
            wraplength=150
        )
        city_label.pack(side=LEFT)

        ## Weather summary frame
        summary_frame = Frame(location_temp_frame, bg="#282829", padx=10, pady=5, highlightbackground="white", highlightthickness=1, cursor="hand2")
        summary_frame.pack(side=LEFT, padx=10, fill=X, expand=True)

        # Create container frames for both views
        weather_view = Frame(summary_frame, bg="#282829")
        time_view = Frame(summary_frame, bg="#282829")

        # Variable to track current view
        self.is_weather_view = True

        def toggle_view(event):
            if self.is_weather_view:
                weather_view.pack_forget()
                time_view.pack(fill=X)
            else:
                time_view.pack_forget()
                weather_view.pack(fill=X)
            self.is_weather_view = not self.is_weather_view

        def bind_recursive(widget, event, callback):
            widget.bind(event, callback)
            for child in widget.winfo_children():
                bind_recursive(child, event, callback)

        # Bind click event to summary_frame and all its children
        bind_recursive(summary_frame, '<Button-1>', toggle_view)

        # Current weather description
        weather_desc = self.data['current']['weather'][0]['description']
        weather_main = self.data['current']['weather'][0]['main']
        daily_summary = self.data['daily'][0]['summary']

        # WEATHER VIEW
        desc_frame = Frame(weather_view, bg="#282829")
        desc_frame.pack()

        summary_label = Label(
            desc_frame,
            text=weather_main,
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#282829"
        )
        summary_label.pack(side=LEFT)

        description_label = Label(
            desc_frame,
            text=f"({weather_desc.capitalize()})",
            font=("Helvetica", 12),
            fg="#57adff",
            bg="#282829"
        )
        description_label.pack(side=LEFT, padx=(10,0), pady=(4,0))

        # Daily Summary Frame
        daily_summary_frame = Frame(weather_view, bg="#282829")
        daily_summary_frame.pack(fill=X, pady=(5,0))

        daily_summary_label = Label(
            daily_summary_frame,
            text=daily_summary,
            font=("Helvetica", 11),
            fg="#e0e0e0",
            bg="#282829",
            wraplength=300,  
            justify=LEFT
        )
        daily_summary_label.pack()
        
        # aqi frame
        aqi_frame = Frame(weather_view, bg="#282829")
        aqi_frame.pack()
        
        aqi_value, aqi_status = get_aqi(self.location)
        
        aqi_label = Label(
            aqi_frame,
            text="Air Quality Index:",
            font=("Helvetica", 12),
            fg="white",
            bg="#282829"
        ) 
        aqi_label.pack(side=LEFT)

        aqi_value = Label(
            aqi_frame,
            text=aqi_value,
            font=("Helvetica", 14, "bold"),
            fg=aqi_status[1],
            bg="#282829"
        )
        aqi_value.pack(side=LEFT, padx=(5,5))

        aqi_status = Label(
            aqi_frame,
            text=aqi_status[0],
            font=("Helvetica", 10),
            fg=aqi_status[1],
            bg="#282829"
        )
        aqi_status.pack(side=LEFT)
        
        # TIME VIEW
        def format_time(timestamp):
            return datetime.fromtimestamp(timestamp).strftime('%H:%M')

        # Sun and Moon times
        sun_moon_frame = Frame(time_view, bg="#282829")
        sun_moon_frame.pack(fill=X, pady=5)

        # Sun Frame
        sun_frame = Frame(sun_moon_frame, bg="#282829")
        sun_frame.pack(side=LEFT, expand=True, fill=X)

        # Sun icon
        sun_icon = "☀️"  # You can replace this with an actual icon image
        sun_label = Label(sun_frame, text=sun_icon, font=("Helvetica", 16), bg="#282829", fg="yellow")
        sun_label.pack()

        sunrise_time = format_time(self.data['daily'][0]['sunrise'])
        sunset_time = format_time(self.data['daily'][0]['sunset'])

        sunrise_label = Label(
            sun_frame,
            text=f"Sunrise: {sunrise_time}",
            font=("Helvetica", 12),
            bg="#282829",
            fg="white"
        )
        sunrise_label.pack()

        sunset_label = Label(
            sun_frame,
            text=f"Sunset: {sunset_time}",
            font=("Helvetica", 12),
            bg="#282829",
            fg="white"
        )
        sunset_label.pack()

        # Moon Frame
        moon_frame = Frame(sun_moon_frame, bg="#282829")
        moon_frame.pack(side=LEFT, expand=True, fill=X)

        # Moon icon
        moon_icon = "🌙"  # You can replace this with an actual icon image
        moon_label = Label(moon_frame, text=moon_icon, font=("Helvetica", 16), bg="#282829")
        moon_label.pack()

        moonrise_time = format_time(self.data['daily'][0]['moonrise'])
        moonset_time = format_time(self.data['daily'][0]['moonset'])

        moonrise_label = Label(
            moon_frame,
            text=f"Moonrise: {moonrise_time}",
            font=("Helvetica", 12),
            bg="#282829",
            fg="white"
        )
        moonrise_label.pack()

        moonset_label = Label(
            moon_frame,
            text=f"Moonset: {moonset_time}",
            font=("Helvetica", 12),
            bg="#282829",
            fg="white"
        )
        moonset_label.pack()

        # Initially show weather view
        weather_view.pack(fill=X)

        ## Temperature display
        temp_frame = Frame(location_temp_frame, bg="#282829", padx=20, highlightbackground="white", highlightthickness=1, pady=10)
        temp_frame.pack(side=RIGHT, padx=(10, 30), pady=15)

        temp_icon_frame = Frame(temp_frame, bg="#282829")
        temp_icon_frame.pack()

        # Cập nhật sự kiện cho temp_frame
        # Thay thế trực tiếp trong sự kiện bind
        temp_frame.bind("<Button-1>", lambda e: self.show_new_weather_details())


        img = (Image.open(self.icon_current_weather(get_current_time(self.location))) )
        self.weather_icon = ImageTk.PhotoImage(img.resize((70, 70)))
        self.icon_label = Label(temp_icon_frame, image=self.weather_icon, bg="#282829")
        self.icon_label.pack(side=LEFT, padx=(0, 10)) 

        self.temp = Label(temp_icon_frame, font=("Helvetica", 40, "bold"), fg="white", bg="#282829")
        self.temp.pack(side=LEFT)

        self.tempDN = Label(temp_frame, font=("Helvetica", 12), fg="#57adff", bg="#282829")
        self.tempDN.pack()

        # Weather details grid
        # details_frame = Frame(main_frame, bg="#F0F2F6")
        details_frame = Frame(main_frame, bg="#57adff")
        details_frame.pack(fill=BOTH, expand=True)

        # Create grid of info cards
        card_frame1 = Frame(details_frame, bg="#57adff")
        card_frame1.pack(fill=X, pady=(15,10))
        card_frame2 = Frame(details_frame, bg="#57adff")
        card_frame2.pack(fill=X)

        # Create info cards
        pressure_card, self.pressure_value = self.create_info_card(card_frame1, "Pressure", "hPa", "icon_weather/pressure_white.png")
        humidity_card, self.humidity_value = self.create_info_card(card_frame1, "Humidity", "%", "icon_weather/humidity_white.png")
        clouds_card, self.clouds_value = self.create_info_card(card_frame1, "Clouds", "%", "icon_weather/clouds_white.png")
        
        pressure_card.pack(side=LEFT, padx=10, expand=True)
        humidity_card.pack(side=LEFT, padx=10, expand=True)
        clouds_card.pack(side=LEFT, padx=10, expand=True)

        uvi_card, self.uvi_value = self.create_info_card(card_frame2, "UV Index", "index", "icon_weather/uvi_white.png")
        visibility_card, self.visibility_value = self.create_info_card(card_frame2, "Visibility", "km", "icon_weather/visibility_white.png")
        wind_card, self.wind_value = self.create_info_card(card_frame2, "Wind Speed", "m/s", "icon_weather/windy_white.png")
        
        uvi_card.pack(side=LEFT, padx=10, expand=True)
        visibility_card.pack(side=LEFT, padx=10, expand=True)
        wind_card.pack(side=LEFT, padx=10, expand=True)
