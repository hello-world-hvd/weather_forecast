import json
import os
from tkinter import*
import tkinter as tk
from turtle import update
from typing import Any
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
from api_getdata import get_json_data
from datetime import datetime

class Favorite:
    def __init__(self, root, data, time_update_id, city, location):
        self.root = root
        self.root.title("Location Information")
        self.data = data
        self.city = city
        self.location = location
        self.time_update_id = time_update_id
        self.create_saved_interface()
        self.update_clock()
        
        # Đọc file JSON
        with open("location_data.json", "r") as f:
            self.locations = json.load(f)
        
        # Tạo các nút cho từng vị trí
        for idx, location in enumerate(self.locations):
            icon_image = Image.open("Images/location_white.png").resize((20, 20))  # Kích thước icon
            icon = ImageTk.PhotoImage(icon_image)

            btn = tk.Button(
                self.root,
                text=location["name"],
                image=icon,
                compound="left",  # Đặt icon bên trái văn bản
                font=("Helvetica", 14, "bold"),
                bg="#282829",
                fg="white",
                activebackground="#3498db",
                activeforeground="white",
                relief="solid", bd=1,
                command=lambda loc=location: self.switch_to_main_interface(loc)
            )
            btn.image = icon  # Giữ tham chiếu để không bị thu gom bộ nhớ
            btn.pack(pady=10)
    
    def switch_to_main_interface(self, location):
        for widget in self.root.winfo_children():
            widget.destroy()
        from weather import WeatherApp
        loc=type('Location', (object,), {
                'latitude': location['latitude'],
                'longitude': location['longitude']
            })
        Main = WeatherApp(self.root, get_json_data(loc), self.time_update_id, location['name'], loc)
        Main.create_main_interface(location["name"], self.data, loc)

    def back_to_main_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from weather import WeatherApp
        Main = WeatherApp(self.root, self.data, self.time_update_id, self.city, self.location)
        Main.create_main_interface(self.city, self.data, self.location)
    
    def update_clock(self):
        # Lấy ngày và giờ hiện tại
        self.current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.clock_label.config(text=self.current_time)
        self.clock_label.after(1000, self.update_clock)
    
    def create_saved_interface(self):

        # Top bar
        top_frame = Frame(self.root, bg="#57adff", height=80)
        top_frame.pack(fill=X)

        # Home button
        img = Image.open("Images/home.png")
        home_resize = img.resize((70, 70))
        home = ImageTk.PhotoImage(home_resize)
        home_button = Button(
            # top_frame,
            image=home,
            borderwidth=0,
            cursor="hand2",
            bg="#57adff",
            activebackground="#57adff",
            command=lambda: self.back_to_main_interface()
        )
        home_button.image = home
        home_button.place(x=900, y=20)
        
        img3 = Image.open("Images/wave1.png")
        img3_resize = img3.resize((750, 532))
        deco3 = ImageTk.PhotoImage(img3_resize)
        Label3 = Label(
            # top_frame,
            image=deco3,
            borderwidth=0,
            bg="#57adff"
        )
        Label3.image=deco3
        Label3.place(x=0, y=150)

        #image1
        img1 = Image.open("Images/sun1.png")
        img1_resize = img1.resize((300, 500))
        deco1 = ImageTk.PhotoImage(img1_resize)
        # canvas.create_image(722, 100, image=deco1)
        Label1 = Label(
            # top_frame,
            image=deco1,
            borderwidth=0,
            bg="#57adff"
        )
        Label1.image=deco1
        Label1.place(x=722, y=100)

        #image2
        img2 = Image.open("Images/sun2.png")
        img2_resize = img2.resize((350, 350))
        deco2 = ImageTk.PhotoImage(img2_resize)
        Label2 = Label(
            # top_frame,
            image=deco2,
            borderwidth=0,
            bg="#57adff"
        )
        Label2.image=deco2
        Label2.place(x=0, y=0)

        # Clock
        self.clock_label = Label(font=("Helvetica", 40, 'bold'), bg="#57adff", fg="white")
        self.clock_label.place(x = 250, y = 20)