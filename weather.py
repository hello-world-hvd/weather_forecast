from tkinter import*
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from numpy import resize
from timezonefinder import TimezoneFinder
from datetime import*
import pytz
import customtkinter
from PIL import Image, ImageTk
from api_getdata import get_json_data, load_location

class WeatherApp:
    def __init__(self, root=None, data=None, time_update_id=None, city=None, location = None):
        if root is None:
            self.root = Tk()
            self.city = None
            self.data = None
            self.location = None
            self.time_update_id = None
        else:
            self.root = root
            self.city = city
            self.data = data
            self.location = location
            self.time_update_id = time_update_id
        self.setup_main_window()
        self.create_main_interface()
        self.city = None
        self.location = None
        
    def setup_main_window(self):
        self.root.title("Weather App")
        self.root.geometry("1000x528+100+50")
        self.root.configure(bg="#57adff")
        self.root.resizable(False, False)

        ##icon
        self.image_icon=PhotoImage(file="Images/logo.png")
        self.root.iconphoto(False, self.image_icon)

    def switch_to_saved_location(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from Interface2 import Favorite
        Favorite(self.root, self.data, self.city, self.time_update_id, self.location)

    def switch_to_detail_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from Interface1 import WeatherDetail
        WeatherDetail(self.root, self.data, self.city, self.time_update_id, self.location)

    def getTime(self, location):
        global time_update_id, clock

        obj=TimezoneFinder()

        result=obj.timezone_at(lng=location.longitude, lat=location.latitude)

        self.timezone.config(text=result)
        self.long_lat.config(text=f"{round(location.latitude, 4)}°N,{round(location.longitude, 4)}°E")

        home=pytz.timezone(result)
        local_time=datetime.now(home)
        current_time=local_time.strftime("%I:%M %p")
        self.clock.config(text=current_time)

        if self.time_update_id is not None:
            self.clock.after_cancel(self.time_update_id)

        self.time_update_id = self.clock.after(1000, self.getTime, location)

    def getWeather(self, json_data):
        # current
        self.temp=json_data['current']['temp']
        self.humidity=json_data['current']['humidity']
        self.pressure=json_data['current']['pressure']
        self.wind=json_data['current']['wind_speed']
        self.description=json_data['current']['weather'][0]['description']
        
        self.t.config(text=(self.temp,"°C"))
        self.h.config(text=(self.humidity,"%"))
        self.p.config(text=(self.pressure,"hPa"))
        self.w.config(text=(self.wind, "m/s"))
        self.d.config(text=self.description)

        #first cell
        self.firstdayimage=json_data['daily'][0]['weather'][0]['icon']
        self.photo1=ImageTk.PhotoImage(file=f"icon/{self.firstdayimage}@2x.png")
        self.firstimage.config(image=self.photo1)
        self.firstimage.image=self.photo1

        self.tempday1 = json_data['daily'][0]['temp']['day']
        self.tempnight1 = json_data['daily'][0]['temp']['night']

        self.day1temp.config(text=f"Day:{self.tempday1}°C \nNight:{self.tempnight1}°C")

        #second cell
        self.seconddayimage=json_data['daily'][1]['weather'][0]['icon']
        img=(Image.open(f"icon/{self.seconddayimage}@2x.png"))
        resized_image=img.resize((50,50))
        self.photo2=ImageTk.PhotoImage(resized_image)
        self.secondimage.config(image=self.photo2)
        self.secondimage.image=self.photo2

        self.tempday2 = json_data['daily'][1]['temp']['day']
        self.tempnight2 = json_data['daily'][1]['temp']['night']

        self.day2temp.config(text=f"Day:{self.tempday2}°C \nNight:{self.tempnight2}°C")

        #third cell
        self.thirddayimage=json_data['daily'][2]['weather'][0]['icon']
        img=(Image.open(f"icon/{self.thirddayimage}@2x.png"))
        resized_image=img.resize((50,50))
        self.photo3=ImageTk.PhotoImage(resized_image)
        self.thirdimage.config(image=self.photo3)
        self.thirdimage.image=self.photo3

        self.tempday3 = json_data['daily'][2]['temp']['day']
        self.tempnight3 = json_data['daily'][2]['temp']['night']

        self.day3temp.config(text=f"Day:{self.tempday3}°C \nNight:{self.tempnight3}°C")

        #fourth cell
        self.fourthdayimage=json_data['daily'][3]['weather'][0]['icon']
        img=(Image.open(f"icon/{self.fourthdayimage}@2x.png"))
        resized_image=img.resize((50,50))
        self.photo4=ImageTk.PhotoImage(resized_image)
        self.fourthimage.config(image=self.photo4)
        self.fourthimage.image=self.photo4

        self.tempday4 = json_data['daily'][3]['temp']['day']
        self.tempnight4 = json_data['daily'][3]['temp']['night']

        self.day4temp.config(text=f"Day:{self.tempday4}°C \nNight:{self.tempnight4}°C")

        #fifth cell
        self.fifthdayimage=json_data['daily'][4]['weather'][0]['icon']
        img=(Image.open(f"icon/{self.fifthdayimage}@2x.png"))
        resized_image=img.resize((50,50))
        self.photo5=ImageTk.PhotoImage(resized_image)
        self.fifthimage.config(image=self.photo5)
        self.fifthimage.image=self.photo5

        self.tempday5 = json_data['daily'][4]['temp']['day']
        self.tempnight5 = json_data['daily'][4]['temp']['night']

        self.day5temp.config(text=f"Day:{self.tempday5}°C \nNight:{self.tempnight5}°C")

        #sixth cell
        self.sixthdayimage=json_data['daily'][5]['weather'][0]['icon']
        img=(Image.open(f"icon/{self.sixthdayimage}@2x.png"))
        resized_image=img.resize((50,50))
        self.photo6=ImageTk.PhotoImage(resized_image)
        self.sixthimage.config(image=self.photo6)
        self.sixthimage.image=self.photo6

        self.tempday6 = json_data['daily'][5]['temp']['day']
        self.tempnight6 = json_data['daily'][5]['temp']['night']

        self.day6temp.config(text=f"Day:{self.tempday6}°C \nNight:{self.tempnight6}°C")

        #seventh cell
        self.seventhdayimage=json_data['daily'][6]['weather'][0]['icon']
        img=(Image.open(f"icon/{self.seventhdayimage}@2x.png"))
        resized_image=img.resize((50,50))
        self.photo7=ImageTk.PhotoImage(resized_image)
        self.seventhimage.config(image=self.photo7)
        self.seventhimage.image=self.photo7

        self.tempday7 = json_data['daily'][6]['temp']['day']
        self.tempnight7 = json_data['daily'][6]['temp']['night']

        self.day7temp.config(text=f"Day:{self.tempday7}°C \nNight:{self.tempnight7}°C")

        #days

        first =datetime.now()
        self.day1.config(text=first.strftime("%d/%m/%Y \n%A"))

        second=first+timedelta(1)
        self.day2.config(text=second.strftime("%d/%m/%Y \n%A"))

        third=first+timedelta(2)
        self.day3.config(text=third.strftime("%d/%m/%Y \n%A"))

        fourth=first+timedelta(3)
        self.day4.config(text=fourth.strftime("%d/%m/%Y \n%A"))

        fifth=first+timedelta(4)
        self.day5.config(text=fifth.strftime("%d/%m/%Y \n%A"))

        sixth=first+timedelta(5)
        self.day6.config(text=sixth.strftime("%d/%m/%Y \n%A"))

        seventh=first+timedelta(6)
        self.day7.config(text=seventh.strftime("%d/%m/%Y \n%A"))

    def getData(self):
        self.city = self.textfield.get()
        self.location = load_location(self.city)
        self.data=get_json_data(self.location)
        self.getTime(self.location)
        self.getWeather(self.data)

    def create_main_interface(self, city=None, json_data=None, location=None):
        for widget in self.root.winfo_children():
            widget.destroy()

        img=(Image.open("Images/Rounded Rectangle 1.png"))
        Round_box_resize=img.resize((250, 115))
        self.Round_box=ImageTk.PhotoImage(Round_box_resize)
        Label(self.root,image=self.Round_box, bg="#57adff").place(x=50, y=130)

        #Menu Button
        top_frame = Frame(self.root, bg="#57adff", height=80)
        top_frame.pack(fill=X)

        menu = Image.open("Images/menu_white.png")
        menu_resize = menu.resize((40, 40))
        menu = ImageTk.PhotoImage(menu_resize)
        menu_button = Button(
            top_frame,
            image=menu,
            borderwidth=0,
            cursor="hand2",
            bg="#57adff",
            activebackground="#57adff",
            command=self.switch_to_saved_location
        )
        menu_button.image = menu
        menu_button.place(x=10, y=10)

        #label
        self.label1=Label(self.root, text="Temperature", font=('Helvetica', 11), fg="white", bg="#203243")
        self.label1.place(x=70, y=140)

        self.label2=Label(self.root, text="Humidity", font=('Helvetica', 11), fg="white", bg="#203243")
        self.label2.place(x=70, y=160)

        self.label3=Label(self.root, text="Presure", font=('Helvetica', 11), fg="white", bg="#203243")
        self.label3.place(x=70, y=180)

        self.label4=Label(self.root, text="Wind Speed", font=('Helvetica', 11), fg="white", bg="#203243")
        self.label4.place(x=70, y=200)

        self.label5=Label(self.root, text="Description", font=('Helvetica', 11), fg="white", bg="#203243")
        self.label5.place(x=70, y=220)

        ##search box
        self.Search_image=PhotoImage(file="Images/Rounded Rectangle 3.png")
        self.myimage=Label(image=self.Search_image, bg="#57adff")
        self.myimage.place(x=370, y=150)

        self.weat_image=PhotoImage(file="Images/Layer 7.png")
        self.weatherimage=Label(self.root, image=self.weat_image, bg="#203243")
        self.weatherimage.place(x=390, y=157)

        self.textfield=tk.Entry(self.root, justify='center', width=15, font=('poppins', 25, 'bold'), bg="#203243", border=0, fg="white")
        self.textfield.place(x=470, y=160)
        if city is not None:
            self.textfield.insert(0, city)
        self.textfield.focus()

        self.Search_icon=PhotoImage(file="Images/Layer 6.png")
        self.myimage_icon=Button(image=self.Search_icon, borderwidth=0, cursor="hand2", bg="#203243", command=self.getData)
        self.myimage_icon.place(x=745, y=155)

        ##Bottom box
        frame = Frame(self.root, width=1010, height=202, bg="#212120")
        frame.pack(side=BOTTOM)

        ##bottom boxes
        #
        img=(Image.open("Images/Rounded Rectangle 2.png"))
        firstbox_resize=img.resize((265, 154))
        self.firstbox=ImageTk.PhotoImage(firstbox_resize)
        
        img=(Image.open("Images/Rounded Rectangle 2 copy.png"))
        secondbox_resize=img.resize((86, 136))
        self.secondbox=ImageTk.PhotoImage(secondbox_resize)
        
        Label(frame, image=self.firstbox, bg="#212120").place(x=30, y=20)
        Label(frame, image=self.secondbox, bg="#212120").place(x=330, y=30)
        Label(frame, image=self.secondbox, bg="#212120").place(x=440, y=30)
        Label(frame, image=self.secondbox, bg="#212120").place(x=550, y=30)
        Label(frame, image=self.secondbox, bg="#212120").place(x=660, y=30)
        Label(frame, image=self.secondbox, bg="#212120").place(x=770, y=30)
        Label(frame, image=self.secondbox, bg="#212120").place(x=880, y=30)

        #clock (here we will place time)
        self.clock=Label(self.root, font=("Helvetica", 35, 'bold'), fg="white", bg="#57adff")
        self.clock.place(x=50, y=40)

        #timezone
        self.timezone=Label(self.root, font=("Helvetica", 25), fg="white", bg="#57adff")
        self.timezone.place(x=700, y=40)

        self.long_lat=Label(self.root, font=("Helvetica", 15), fg="white", bg="#57adff")
        self.long_lat.place(x=700, y=80)

        #thpwd
        self.t=Label(self.root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
        self.t.place(x=170, y=140)

        self.h=Label(self.root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
        self.h.place(x=170, y=160)

        self.p=Label(self.root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
        self.p.place(x=170, y=180)

        self.w=Label(self.root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
        self.w.place(x=170, y=200)

        self.d=Label(self.root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
        self.d.place(x=170, y=220)

        # first cell
        self.firstframe = Frame(self.root, width=260, height=150, bg="#282829", cursor="hand2")
        self.firstframe.place(x=35, y=350)

        # Add click binding to the entire frame
        self.firstframe.bind('<Button-1>', lambda e: self.switch_to_detail_interface())

        self.day1 = Label(self.firstframe, font="arial 20", bg="#282829", fg="#fff")
        self.day1.place(x=100, y=5)
        self.day1.bind('<Button-1>', lambda e: self.switch_to_detail_interface())

        self.firstimage = Label(self.firstframe, bg="#282829")
        self.firstimage.place(x=2, y=40)
        self.firstimage.bind('<Button-1>', lambda e: self.switch_to_detail_interface())

        self.day1temp = Label(self.firstframe, bg="#282829", fg="#57adff", font="arial 15 bold")
        self.day1temp.place(x=100, y=75)
        self.day1temp.bind('<Button-1>', lambda e: self.switch_to_detail_interface())
        #second cell
        self.secondframe=Frame(self.root, width=80, height=130, bg="#282829")
        self.secondframe.place(x=335, y=360)

        self.day2=Label(self.secondframe, bg="#282829", fg="#fff")
        self.day2.place(x=10, y=5)

        self.secondimage=Label(self.secondframe, bg="#282829")
        self.secondimage.place(x=7, y=40)

        self.day2temp=Label(self.secondframe, bg="#282829", fg="#fff")
        self.day2temp.place(x=2, y=90)

        #third cell
        self.thirdframe=Frame(self.root, width=80, height=130, bg="#282829")
        self.thirdframe.place(x=445, y=360)

        self.day3=Label(self.thirdframe, bg="#282829", fg="#fff")
        self.day3.place(x=10, y=5)

        self.thirdimage=Label(self.thirdframe, bg="#282829")
        self.thirdimage.place(x=7, y=40)

        self.day3temp=Label(self.thirdframe, bg="#282829", fg="#fff")
        self.day3temp.place(x=2, y=90)

        #fourth cell
        self.fourthframe=Frame(self.root, width=80, height=130, bg="#282829")
        self.fourthframe.place(x=555, y=360)

        self.day4=Label(self.fourthframe, bg="#282829", fg="#fff")
        self.day4.place(x=10, y=5)

        self.fourthimage=Label(self.fourthframe, bg="#282829")
        self.fourthimage.place(x=7, y=40)

        self.day4temp=Label(self.fourthframe, bg="#282829", fg="#fff")
        self.day4temp.place(x=2, y=90)

        #fifth cell
        self.fifthframe=Frame(self.root, width=80, height=130, bg="#282829")
        self.fifthframe.place(x=665, y=360)

        self.day5=Label(self.fifthframe, bg="#282829", fg="#fff")
        self.day5.place(x=10, y=5)

        self.fifthimage=Label(self.fifthframe, bg="#282829")
        self.fifthimage.place(x=7, y=40)

        self.day5temp=Label(self.fifthframe, bg="#282829", fg="#fff")
        self.day5temp.place(x=2, y=90)

        #sixth cell
        self.sixthframe=Frame(self.root, width=80, height=130, bg="#282829")
        self.sixthframe.place(x=775, y=360)

        self.day6=Label(self.sixthframe, bg="#282829", fg="#fff")
        self.day6.place(x=10, y=5)

        self.sixthimage=Label(self.sixthframe, bg="#282829")
        self.sixthimage.place(x=7, y=40)

        self.day6temp=Label(self.sixthframe, bg="#282829", fg="#fff")
        self.day6temp.place(x=2, y=90)

        #seventh cell
        self.seventhframe=Frame(self.root, width=80, height=130, bg="#282829")
        self.seventhframe.place(x=885, y=360)

        self.day7=Label(self.seventhframe, bg="#282829", fg="#fff")
        self.day7.place(x=10, y=5)

        self.seventhimage=Label(self.seventhframe, bg="#282829")
        self.seventhimage.place(x=7, y=40)

        self.day7temp=Label(self.seventhframe, bg="#282829", fg="#fff")
        self.day7temp.place(x=2, y=90)

        if city is not None:
            self.getWeather(json_data)
            self.getTime(location)
            print(city)


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WeatherApp()

    app.run()
