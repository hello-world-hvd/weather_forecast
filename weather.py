import json
from tkinter import*
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from numpy import resize
from timezonefinder import TimezoneFinder
from datetime import*
import requests
import pytz
from PIL import Image, ImageTk

root=Tk()
root.title("Weather App")
# root.geometry("890x470+300+200")
root.geometry("1000x528+100+50")
root.configure(bg="#57adff")
root.resizable(False, False)

def getWeather():
    city=textfield.get()

    geolocator=Nominatim(user_agent="geoapiExercises")
    try:
        location=geolocator.geocode(city)
        if location is None:
            print("notfound city")
            return
    except Exception as e:
        print(f"Error lỗi khi tìm kiếm vị trí: {e}")
        return
    obj=TimezoneFinder()

    result=obj.timezone_at(lng=location.longitude, lat=location.latitude)

    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude, 4)}°N,{round(location.longitude, 4)}°E")

    home=pytz.timezone(result)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    #weather
    api="https://api.openweathermap.org/data/2.8/onecall?lat="+str(location.latitude)+"&lon="+str(location.longitude)+"&units=metric&exclude=hourly&appid=a40a08819e2ca4455e9badc3a50026b6"
    json_data=requests.get(api).json()

    # current
    temp=json_data['current']['temp']
    humidity=json_data['current']['humidity']
    pressure=json_data['current']['pressure']
    wind=json_data['current']['wind_speed']
    description=json_data['current']['weather'][0]['description']
    
    t.config(text=(temp,"°C"))
    h.config(text=(humidity,"%"))
    p.config(text=(pressure,"hPa"))
    w.config(text=(wind, "m/s"))
    d.config(text=description)

    #first cell
    firstdayimage=json_data['daily'][0]['weather'][0]['icon']
    photo1=ImageTk.PhotoImage(file=f"icon/{firstdayimage}@2x.png")
    firstimage.config(image=photo1)
    firstimage.image=photo1

    tempday1 = json_data['daily'][0]['temp']['day']
    tempnight1 = json_data['daily'][0]['temp']['night']

    day1temp.config(text=f"Day:{tempday1}°C \nNight:{tempnight1}°C")

    #second cell
    seconddayimage=json_data['daily'][1]['weather'][0]['icon']
    img=(Image.open(f"icon/{seconddayimage}@2x.png"))
    resized_image=img.resize((50,50))
    photo2=ImageTk.PhotoImage(resized_image)
    secondimage.config(image=photo2)
    secondimage.image=photo2

    tempday2 = json_data['daily'][1]['temp']['day']
    tempnight2 = json_data['daily'][1]['temp']['night']

    day2temp.config(text=f"Day:{tempday2}°C \nNight:{tempnight2}°C")

    #third cell
    thirddayimage=json_data['daily'][2]['weather'][0]['icon']
    img=(Image.open(f"icon/{thirddayimage}@2x.png"))
    resized_image=img.resize((50,50))
    photo3=ImageTk.PhotoImage(resized_image)
    thirdimage.config(image=photo3)
    thirdimage.image=photo3

    tempday3 = json_data['daily'][2]['temp']['day']
    tempnight3 = json_data['daily'][2]['temp']['night']

    day3temp.config(text=f"Day:{tempday3}°C \nNight:{tempnight3}°C")

    #fourth cell
    fourthdayimage=json_data['daily'][3]['weather'][0]['icon']
    img=(Image.open(f"icon/{fourthdayimage}@2x.png"))
    resized_image=img.resize((50,50))
    photo4=ImageTk.PhotoImage(resized_image)
    fourthimage.config(image=photo4)
    fourthimage.image=photo4

    tempday4 = json_data['daily'][3]['temp']['day']
    tempnight4 = json_data['daily'][3]['temp']['night']

    day4temp.config(text=f"Day:{tempday4}°C \nNight:{tempnight4}°C")

    #fifth cell
    fifthdayimage=json_data['daily'][4]['weather'][0]['icon']
    img=(Image.open(f"icon/{fifthdayimage}@2x.png"))
    resized_image=img.resize((50,50))
    photo5=ImageTk.PhotoImage(resized_image)
    fifthimage.config(image=photo5)
    fifthimage.image=photo5

    tempday5 = json_data['daily'][4]['temp']['day']
    tempnight5 = json_data['daily'][4]['temp']['night']

    day5temp.config(text=f"Day:{tempday5}°C \nNight:{tempnight5}°C")

    #sixth cell
    sixthdayimage=json_data['daily'][5]['weather'][0]['icon']
    img=(Image.open(f"icon/{sixthdayimage}@2x.png"))
    resized_image=img.resize((50,50))
    photo6=ImageTk.PhotoImage(resized_image)
    sixthimage.config(image=photo6)
    sixthimage.image=photo6

    tempday6 = json_data['daily'][5]['temp']['day']
    tempnight6 = json_data['daily'][5]['temp']['night']

    day6temp.config(text=f"Day:{tempday6}°C \nNight:{tempnight6}°C")

    #seventh cell
    seventhdayimage=json_data['daily'][6]['weather'][0]['icon']
    img=(Image.open(f"icon/{seventhdayimage}@2x.png"))
    resized_image=img.resize((50,50))
    photo7=ImageTk.PhotoImage(resized_image)
    seventhimage.config(image=photo7)
    seventhimage.image=photo7

    tempday7 = json_data['daily'][6]['temp']['day']
    tempnight7 = json_data['daily'][6]['temp']['night']

    day7temp.config(text=f"Day:{tempday7}°C \nNight:{tempnight7}°C")

    #days

    first =datetime.now()
    day1.config(text=first.strftime("%A"))

    second=first+timedelta(1)
    day2.config(text=second.strftime("%A"))

    third=first+timedelta(2)
    day3.config(text=third.strftime("%A"))

    fourth=first+timedelta(3)
    day4.config(text=fourth.strftime("%A"))

    fifth=first+timedelta(4)
    day5.config(text=fifth.strftime("%A"))

    sixth=first+timedelta(5)
    day6.config(text=sixth.strftime("%A"))

    seventh=first+timedelta(6)
    day7.config(text=seventh.strftime("%A"))

##icon
image_icon=PhotoImage(file="Images/logo.png")
root.iconphoto(False, image_icon)

# Round_box=PhotoImage(file="Images/Rounded Rectangle 1.png")
img=(Image.open("Images/Rounded Rectangle 1.png"))
Round_box_resize=img.resize((250, 115))
Round_box=ImageTk.PhotoImage(Round_box_resize)
# Label(root,image=Round_box, bg="#57adff").place(x=30, y=110)
Label(root,image=Round_box, bg="#57adff").place(x=50, y=130)

#label
label1=Label(root, text="Temperature", font=('Helvetica', 11), fg="white", bg="#203243")
# label1.place(x=50, y=120)
label1.place(x=70, y=140)

label2=Label(root, text="Humidity", font=('Helvetica', 11), fg="white", bg="#203243")
label2.place(x=70, y=160)

label3=Label(root, text="Presure", font=('Helvetica', 11), fg="white", bg="#203243")
label3.place(x=70, y=180)

label4=Label(root, text="Wind Speed", font=('Helvetica', 11), fg="white", bg="#203243")
label4.place(x=70, y=200)

label5=Label(root, text="Description", font=('Helvetica', 11), fg="white", bg="#203243")
label5.place(x=70, y=220)

##search box
Search_image=PhotoImage(file="Images/Rounded Rectangle 3.png")
myimage=Label(image=Search_image, bg="#57adff")
# myimage.place(x=320, y=120)
myimage.place(x=370, y=150)

weat_image=PhotoImage(file="Images/Layer 7.png")
weatherimage=Label(root, image=weat_image, bg="#203243")
# weatherimage.place(x=340, y=127)
weatherimage.place(x=390, y=157)

textfield=tk.Entry(root, justify='center', width=15, font=('poppins', 25, 'bold'), bg="#203243", border=0, fg="white")
# textfield.place(x=420, y=130)
textfield.place(x=470, y=160)
textfield.focus()

Search_icon=PhotoImage(file="Images/Layer 6.png")
myimage_icon=Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#203243", command=getWeather)
# myimage_icon.place(x=695, y=125)
myimage_icon.place(x=745, y=155)

##Bottom box
# frame = Frame(root, width=900, height=180, bg="#212120")
frame = Frame(root, width=1010, height=202, bg="#212120")
frame.pack(side=BOTTOM)

##botton boxes
#
img=(Image.open("Images/Rounded Rectangle 2.png"))
firstbox_resize=img.resize((265, 154))
firstbox=ImageTk.PhotoImage(firstbox_resize)
#
# firstbox=PhotoImage(file="Images/Rounded Rectangle 2.png")
#
img=(Image.open("Images/Rounded Rectangle 2 copy.png"))
secondbox_resize=img.resize((86, 136))
secondbox=ImageTk.PhotoImage(secondbox_resize)
#
# secondbox=PhotoImage(file="Images/Rounded Rectangle 2 copy.png")

# Label(frame, image=firstbox, bg="#212120").place(x=30, y=20)
Label(frame, image=firstbox, bg="#212120").place(x=30, y=20)
# Label(frame, image=secondbox, bg="#212120").place(x=300, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=330, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=440, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=550, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=660, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=770, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=880, y=30)

#clock (here we will place time)
clock=Label(root, font=("Helvetica", 35, 'bold'), fg="white", bg="#57adff")
clock.place(x=50, y=40)


#timezone
timezone=Label(root, font=("Helvetica", 25), fg="white", bg="#57adff")
timezone.place(x=700, y=40)

long_lat=Label(root, font=("Helvetica", 15), fg="white", bg="#57adff")
long_lat.place(x=700, y=80)

#thpwd
t=Label(root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
# t.place(x=150, y=120)
t.place(x=170, y=140)

h=Label(root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
h.place(x=170, y=160)

p=Label(root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
p.place(x=170, y=180)

w=Label(root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
w.place(x=170, y=200)

d=Label(root, text="---", font=("Helvatica", 11), fg="white", bg="#203243")
d.place(x=170, y=220)

# first cell
firstframe=Frame(root, width=260, height=150, bg="#282829")
# firstframe.place(x=35, y=315)
firstframe.place(x=35, y=350)

day1=Label(firstframe, font="arial 20", bg="#282829", fg="#fff")
day1.place(x=100, y=5)

firstimage=Label(firstframe, bg="#282829")
firstimage.place(x=2, y=15)

day1temp=Label(firstframe, bg="#282829", fg="#57adff", font="arial 15 bold")
day1temp.place(x=100, y=50)

#second cell
secondframe=Frame(root, width=80, height=130, bg="#282829")
secondframe.place(x=335, y=360)

day2=Label(secondframe, bg="#282829", fg="#fff")
day2.place(x=10, y=5)

secondimage=Label(secondframe, bg="#282829")
secondimage.place(x=7, y=25)

day2temp=Label(secondframe, bg="#282829", fg="#fff")
day2temp.place(x=2, y=75)

#third cell
thirdframe=Frame(root, width=80, height=130, bg="#282829")
thirdframe.place(x=445, y=360)


day3=Label(thirdframe, bg="#282829", fg="#fff")
day3.place(x=10, y=5)

thirdimage=Label(thirdframe, bg="#282829")
thirdimage.place(x=7, y=25)

day3temp=Label(thirdframe, bg="#282829", fg="#fff")
day3temp.place(x=2, y=75)

#fourth cell
fourthframe=Frame(root, width=80, height=130, bg="#282829")
fourthframe.place(x=555, y=360)


day4=Label(fourthframe, bg="#282829", fg="#fff")
day4.place(x=10, y=5)

fourthimage=Label(fourthframe, bg="#282829")
fourthimage.place(x=7, y=25)

day4temp=Label(fourthframe, bg="#282829", fg="#fff")
day4temp.place(x=2, y=75)

#fifth cell
fifthframe=Frame(root, width=80, height=130, bg="#282829")
fifthframe.place(x=665, y=360)


day5=Label(fifthframe, bg="#282829", fg="#fff")
day5.place(x=10, y=5)

fifthimage=Label(fifthframe, bg="#282829")
fifthimage.place(x=7, y=25)

day5temp=Label(fifthframe, bg="#282829", fg="#fff")
day5temp.place(x=2, y=75)

#sixth cell
sixthframe=Frame(root, width=80, height=130, bg="#282829")
sixthframe.place(x=775, y=360)


day6=Label(sixthframe, bg="#282829", fg="#fff")
day6.place(x=10, y=5)

sixthimage=Label(sixthframe, bg="#282829")
sixthimage.place(x=7, y=25)

day6temp=Label(sixthframe, bg="#282829", fg="#fff")
day6temp.place(x=2, y=75)

#seventh cell
seventhframe=Frame(root, width=80, height=130, bg="#282829")
seventhframe.place(x=885, y=360)

day7=Label(seventhframe, bg="#282829", fg="#fff")
day7.place(x=10, y=5)

seventhimage=Label(seventhframe, bg="#282829")
seventhimage.place(x=7, y=25)

day7temp=Label(seventhframe, bg="#282829", fg="#fff")
day7temp.place(x=2, y=75)






root.mainloop()