#!/usr/bin/python3
import I2C_LCD_driver
import json
from time import *
from mvg_api import *
from pprint import pprint
import requests
import math

mylcd = I2C_LCD_driver.lcd()
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Munich&APPID=bdfa44dcb4524d536a04c4a9db44b902')
whk_id = get_id_for_station('Wilhelm-Kuhnert-Straße')
#should be de:09162:1166
clear = " " * 20
i = 0
d = 0
try:
    erg = str(r.json())
    iter = 0
    inw = False
    done = False
    while iter > len(erg):
        if (erg[iter]=='['):
            inw = True
        elif (not done) and inw and (erg[iter]=='}'):
            done = True
        elif inw and done and (erg[iter]==']'):
            inw = False
            done = False
        elif inw and done:
            erg[iter] = '_'
        iter = iter + 1
    erg = erg.replace('\'','"').replace('[','').replace(']','').replace('_','')
    #print(erg)
    e = json.loads(erg)
    tmp = e['main']['temp'] - 273.15
    weather = '*** ' + str(math.ceil(tmp*10)/10) +' C * ' + e['weather']['description'] + ' * Wind: ' + str(e['wind']['speed']) + ' m/s ***'
except (ValueError, KeyError, TypeError):
    weather = 'Error parsing JSON'
weather = '   ' + weather
while True:
    noconnect = False
    try:
        #print (whk_id)
        departures = get_departures(whk_id)
    except:
        noconnect = True
    c = 1
    mylcd.lcd_display_string(clear,1)
    mylcd.lcd_display_string(clear,2)
    mylcd.lcd_display_string(clear,3)
    if noconnect:
        mylcd.lcd_display_string('No connection!',1)
    else:
        for departure in departures:
            ausgabe = 'Error'
            zeit = -1
            if 'Tierpark' in departure['destination']:
                continue

            elif 'Sendlinger Tor' in departure['destination']:
                ausgabe = 'Sendlinger Tor'
            else:
                ausgabe = departure['destination']
            if (departure['departureTimeMinutes'] == 1439):
                zeit = 0
            else:
                zeit = departure['departureTimeMinutes']
            mylcd.lcd_display_string(departure['label'] + ' ' + ausgabe,c)
            if (zeit < 10):
                mylcd.lcd_display_string(str(zeit),c,19)
            elif (zeit < 100):
                mylcd.lcd_display_string(str(zeit),c,18)
            else:
                mylcd.lcd_display_string(str(zeit),c,17)
            c = c + 1
            if (c > 3):
                break;
    while (i < len(weather)):
        lcd_text = weather[i:(i+20)]
        if (i >= len(weather)-20):
            lcd_text = lcd_text + weather[0:(20+i-len(weather))]
        mylcd.lcd_display_string(lcd_text,4)
        sleep(0.5)
        mylcd.lcd_display_string(clear,4)
        i = i + 1
        d = d + 1
        if (i >= len(weather)):
            i = 0
        if (d%20 == 0):
            break;
    if (d > 6000):
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Munich&APPID=bdfa44dcb4524d536a04c4a9db44b902')
        try:
            erg = str(r.json())
            erg = erg.replace('\'','"').replace('[','').replace(']','')
            e = json.loads(erg)
            tmp = e['main']['temp'] - 273.15
            weather = '*** ' + str(math.ceil(tmp*10)/10) +' C * ' + e['weather']['description'] + ' * Wind: ' + str(e['wind']['speed']) + ' m/s ***'
        except (ValueError, KeyError, TypeError):
            weather = 'Error parsing JSON'
        weather = '   ' + weather
        d = 0
        i = 0
mylcd.lcd_clear()
