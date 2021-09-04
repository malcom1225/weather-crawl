import requests 
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pytz
import json 
from os import path

SLEEP_TIME = 3600
filename = './data.json'
url_weather = "https://weather.com/weather/today/l/10.49,107.25"
url_airquality = "https://weather.com/forecast/air-quality/l/f897f4ac8e6c90b59c95b961403bb9a0041661f33852f68eb6041b5abc25a164"

def get_time():
    now = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    time = {
        'Date':now.strftime("%m/%d/%Y"),
        'Time':now.strftime("%H:%M:%S"),
        'Day': now.strftime('%d'),
        'Month': now.strftime('%m'),
        'Year': now.strftime('%Y'),
    }

    print(time)
    return time

def get_airquality():
    soup = BeautifulSoup(requests.get(url_airquality).content,'html.parser')

    value = soup.find('text',class_="DonutChart--innerValue--2rO41 AirQuality--extendedDialText--2AsJa").text

    quality = soup.find('span',class_="AirQualityText--severity--1fu5k AirQuality--extendedDialCategotyText--1Adwm").text

    pollution = soup.find('div',class_="AirQuality--rightCol--3MRhw").text

    quality_desc = soup.find('p',class_="AirQualityText--severityText--1wT_O AirQuality--extendedDialSeverityText--2rz1B").text

    air_quality = {
        'Pollution': pollution,
        'Pollution_Value': value,
        'Quality': quality,
        'Quality_Description': quality_desc,
    }
    return air_quality

def get_weather():
    soup = BeautifulSoup(requests.get(url_weather).content,'html.parser')

    temp = soup.find('div',class_="CurrentConditions--primary--2SVPh").text

    condition = temp[3:]

    temp = temp[:-len(condition)-1]

    temp = str(int((int(temp)-32)*5/9)) #F to C

    soup = soup.find('div',class_="TodayDetailsCard--detailsContainer--16Hg0")
    soup = soup.find_all('div',class_="WeatherDetailsListItem--wxData--2s6HT")
    for bow in soup:
        child = bow.find("span")
        if "PercentageValue" in child['data-testid']:
            hum = child.text
            break
    
    humidity = hum

    for bow in soup:
        child = bow.find("span")
        if "UVIndexValue" in child['data-testid']:
            uv = child.text
            break
    uvindex = uv

    weather = {
        'Temperature': temp,
        'Condition': condition,
        'Humidity': humidity,
        'UV_Index':uvindex,
    }
    weather.update(get_airquality())

    return weather

def data_prepare():
    
    if path.isfile(filename) is False:
        f =  open(filename,'a')
        f.write("[]")
        f.close()

    with open(filename) as fp:
        list_weather = json.load(fp)

    raw_data = {}
    raw_data.update(get_weather())
    raw_data.update(get_time())

    list_weather.append(raw_data)

    print(raw_data)

    return list_weather

def write_weather(listTemp):
    with open(filename, 'w') as json_file:
        json.dump(listTemp, json_file,indent=4,separators=(',',': '))
    

def main():
    try:
        while True:
            listTemp = []
            listTemp = data_prepare()
            write_weather(listTemp)
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print("terminated!")
        pass

if __name__ == '__main__':
   main()