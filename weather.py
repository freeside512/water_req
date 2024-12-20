import requests
import sys
import urllib
import json
weather_categories = {
    'NORMAL': [
        'cloudy', 'fog', 'hail', 'partly-cloudy-day', 'partly-cloudy-night', 'sleet'
    ],
    'SUNNY': [
        'clear-day', 'clear-night'
    ],
    'WINDY': [
        'wind'
    ],
    'RAINY': [
        'rain', 'rain-snow', 'rain-snow-showers-day', 'rain-snow-showers-night',
        'showers-day', 'showers-night', 'thunder-rain', 'thunder-showers-day',
        'thunder-showers-night', 'snow', 'snow-showers-day', 'snow-showers-night',
        'thunder'
    ]
}

class Weather:
    def __init__(self,latitude,longitude):

        self.latitude = latitude    
        self.longitude = longitude
        self.api = 'UNZ29KE7AN6PDYEF4DT6K4GJT'

    def temp_cond(self):

                
        try: 
            ResultBytes = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self.latitude}%2C{self.longitude}?unitGroup=metric&include=days&key={self.api}&contentType=json&lang=fa")
            ResultBytes2 = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self.latitude}%2C{self.longitude}/2022-08-08/2022-09-09?unitGroup=metric&include=days&key={self.api}&contentType=json")

            jsonData = json.load(ResultBytes)
            jsonData2 = json.load(ResultBytes2)
            self.temp = jsonData['days'][0]['temp']
            self.condition = jsonData['days'][0]['conditions']
            self.icon = jsonData['days'][0]['icon']
            for i in weather_categories:
                if self.icon in weather_categories[i]:
                    self.send_cond = i

            if self.temp<20:
                self.send_temp = '10-20'
            elif self.temp < 30: 
                self.send_temp = '20-30'
            elif self.temp < 40: 
                self.send_temp = '30-40'
            else:
                self.send_temp = '40-50'

            total_rain = sum(day['precip'] for day in jsonData2['days'])
            if total_rain < 20:
                self.send_region= "DESERT"
            elif total_rain < 40:
                self.send_region= "SEMI ARID"
            elif total_rain < 80:
                self.send_region= "SEMI HUMID"
            else:
                self.send_region= "HUMID"


        except urllib.error.HTTPError  as e:
            ErrorInfo= e.read().decode() 
            print('Error code: ', e.code, ErrorInfo)
            sys.exit()
        except  urllib.error.URLError as e:
            ErrorInfo= e.read().decode() 
            print('Error code: ', e.code,ErrorInfo)
            sys.exit()



