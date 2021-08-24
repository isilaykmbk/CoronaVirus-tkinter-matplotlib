import tkinter as CoronaVirus
from tkinter import *
from tkinter import messagebox as mb
import matplotlib.pyplot as plt
import requests
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
import numpy as np

province = ['ALA Aland Islands', 'American Samoa', 'Anguilla', 'Antarctica', 'Aruba', 'Bermuda', 'Bouvet Island',
            'British Indian Ocean Territory', 'British Virgin Islands', 'Cayman Islands',
            'Christmas Island', 'Cocos (Keeling) Islands', 'Cook Islands', 'Falkland Islands (Malvinas)',
            'Faroe Islands', 'French Guiana', 'French Polynesia', 'French Southern Territories',
            'Gibraltar', 'Greenland', 'Guadeloupe', 'Guam', 'Guernsey', 'Heard and Mcdonald Islands',
            'Hong Kong, SAR China', 'Isle of Man', 'Jersey', 'Kiribati', 'Korea (North)',
            'Macao, SAR China', 'Marshall Islands', 'Martinique', 'Mayotte', 'Micronesia, Federated States of',
            'Montserrat', 'Nauru', 'Netherlands Antilles', 'New Caledonia', 'Niue',
            'Norfolk Island', 'Northern Mariana Islands', 'Palau', 'Pitcairn', 'Puerto Rico', 'Réunion', 'Saint Helena',
            'Saint Pierre and Miquelon', 'Saint-Barthélemy', 'Saint-Martin (French part)',
            'Samoa', 'Solomon Islands', 'South Georgia and the South Sandwich Islands',
            'Svalbard and Jan Mayen Islands', 'Tokelau', 'Tonga', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu',
            'US Minor Outlying Islands', 'Vanuatu', 'Virgin Islands, US',
            'Wallis and Futuna Islands']

window = CoronaVirus.Tk()
window.title("CoronaVirus")
window.geometry("1000x600")
ulkeler = []
cases = []
date = []
dataSelection = ["Confirmed", "Deaths", "Recovered", "Active",
                 "Daily Confirmed", "Daily Deaths", "Daily Recovered", "Daily Active"]

def grafikDetail(event):
    try:
        if 0 < event.xdata < len(cases)//radioButtonV.get():
            xTransform = ax.transData.transform((int(event.xdata), int(event.ydata)))[0]
            yTransform = \
                ax.transData.transform((int(event.xdata), cases[int(event.xdata)]))[1]
        bilgilendirmePaneli.config(
            text="Date: " + str(date[int(event.xdata)]) + " Case: " + str(
                cases[int(event.xdata)]))
        bilgilendirmePaneli.place(x=xTransform+90, y=550 - yTransform)
    except:
        bilgilendirmePaneli.place_forget()
        pass

def fontSize(val):  #Gosterilen eleman sayisina gore font boyu donduren fonksiyon.
    print(val)
    if val <= 50:
        return 10
    elif 50 < val <= 58:
        return 9
    elif 58 < val <= 63:
        return 7
    elif 63 < val <= 80:
        return 6
    elif 80 < val <= 90:
        return 5
    elif 90 < val <= 110:
        return 4
    elif val > 110:
        return 4

def chartButtonShow():
    if ulkeler_list.curselection() != () and data_list.curselection() != ():
        Cases()
        Date()
        ax.cla()
        label = str(ulkeler_list.get(ulkeler_list.curselection())) + " " + str(data_list.get(data_list.curselection()))
        ax.plot(date[0:len(date)//radioButtonV.get()], cases[0:len(date)//radioButtonV.get()], label=label, marker=".")
        ax.legend()
        plt.xlabel("x ekseni")
        plt.ylabel("y ekseni")
        ax.set_title("Graph")
        ax.tick_params(axis='x', labelsize=fontSize(len(cases[0:len(date) // radioButtonV.get()])), labelrotation=-90)
        canvas.draw()
    else:
        mb.showwarning(message="Please select a country and a data type!")

def chartUpdate():
    if len(date) > 0 and len(cases) > 0:
        ax.cla()
        label = str(ulkeler_list.get(ulkeler_list.curselection())) + " " + str(data_list.get(data_list.curselection()))
        ax.plot(date[0:(len(date) // radioButtonV.get())], cases[0:(len(date) // radioButtonV.get())], label=label, marker=".")
        ax.legend()
        ax.set_title("Graph")
        plt.xlabel("x ekseni")
        plt.ylabel("y ekseni")
        ax.tick_params(axis='x', labelsize=fontSize(len(cases[0:len(date) // radioButtonV.get()])), labelrotation=-90)
        canvas.draw()

def country_add():
    try:
        response = requests.get("https://api.covid19api.com/countries")
        jsonFile = response.json()
        global ulkeler
        for i in jsonFile:
            if i["Country"] not in province:
                ulkeDict = {}
                ulkeDict["Country"] = i["Country"]
                ulkeDict["Slug"] = i["Slug"]
                ulkeler.append(ulkeDict)
        ulkeler = (sorted(ulkeler, key=lambda i: i["Country"]))
    except:
        print("basaramadik abi")
        raise

def Cases():
    global cases
    cases = []
    seciliUlke = ulkeler_list.get(ulkeler_list.curselection())
    if seciliUlke == "China":
        url = "https://api.covid19api.com/total/country/china"
    else:
        url = "https://api.covid19api.com/total/dayone/country/" + ulkeler[ulkeler_list.curselection()[0]]["Slug"]
    response = requests.get(url)
    jsonFile = response.json()
    print(url)
    if data_list.get(data_list.curselection()).split(" ")[0] == "Daily":
        dataType = data_list.get(data_list.curselection()).split(" ")[1]
        cases.append(jsonFile[0][str(dataType)])
        for i in range(1, len(jsonFile)):
            dailyCase = jsonFile[i][str(dataType)] - jsonFile[i-1][str(dataType)]
            cases.append(dailyCase)
    else:
        for i in jsonFile:
            print(i)
            cases.append(i[data_list.get(data_list.curselection())])
    print(cases)

def Date():
    global date
    date = []
    seciliUlke = ulkeler_list.get(ulkeler_list.curselection())
    if seciliUlke == "China":
        url = "https://api.covid19api.com/total/country/china"
    else:
        url = "https://api.covid19api.com/total/dayone/country/" + ulkeler[ulkeler_list.curselection()[0]]["Slug"]
    response = requests.get(url)
    jsonFile = response.json()
    for i in jsonFile:
        date.append(i['Date'][6:10])

def RadioButtonUp():
    if radioButtonV.get() - 1 <= 0:
        dateRadioButtons[0].select()
    else:
        dateRadioButtons[5-(radioButtonV.get() - 1)].select()
    chartUpdate()

def RadioButtonDown():
    if radioButtonV.get() + 1 > 5:
        dateRadioButtons[4].select()
    else:
        dateRadioButtons[4-radioButtonV.get()].select()
    chartUpdate()

frame = CoronaVirus.Frame(window, background="gray97", width=1000, height=1000)
frame.pack()
figure = Figure(figsize=(8, 5), dpi=100)
ax = figure.add_subplot(111)
ax.set_title("Graph")
canvas = FigureCanvasTkAgg(figure, frame)
canvas.get_tk_widget().place(x=190, y=50)

label = CoronaVirus.Label(frame, text="Country Selection", font="Calibri 12", background="gray97")
label.place(x=0, y=0)
ulkeler_list = CoronaVirus.Listbox(frame, width=30, height=15, selectmode="SINGLE", relief="groove", background="gray80",
                          exportselection=0)
ulkeler_list.place(x=0, y=30)
country_add()
for i in ulkeler:
    ulkeler_list.insert(END, i["Country"])

label2 = CoronaVirus.Label(frame, text="Data Selection", font="Calibri 12", background="gray97")
label2.place(x=0, y=280)
data_list = CoronaVirus.Listbox(frame, width=30, height=15, selectmode="SINGLE", relief="groove", background="gray80",
                       exportselection=0)
data_list.place(x=0, y=305)
data_list.insert(END, *dataSelection)

bilgilendirmePaneli = Label(frame)

radioButtonV = IntVar()

figure.canvas.mpl_connect('motion_notify_event', grafikDetail)

dateRadioButtons=[]

for i in range(5):
    dateRadioButtons.append(CoronaVirus.Radiobutton(frame, variable=radioButtonV, value=5-i, command=chartUpdate))
    dateRadioButtons[i].place(x=500+50*i, y=550)
dateButtonDown = CoronaVirus.Button(frame, text="<", relief=RAISED, font="Calibri", command=RadioButtonDown)
dateButtonDown.place(x=450, y=550)
dateButtonUp = CoronaVirus.Button(frame, text=">", relief=RAISED, font="Calibri", command=RadioButtonUp)
dateButtonUp.place(x=750, y=550)

dateRadioButtons[0].select()

buton = CoronaVirus.Button(frame, text="Draw", relief=RAISED, font="Calibri", command=chartButtonShow)
buton.place(x=60, y=550)

window.mainloop()