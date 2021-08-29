import requests 
from bs4 import BeautifulSoup
import time
import json 
from os import path

SLEEP_TIME = 900
filename = './data.json'

def get_time():
    now = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())

    return now

def get_airquality():
    soup = BeautifulSoup(requests.get("https://weather.com/forecast/air-quality/l/495b7c9b6fd1597a531b13797693f17973525dbb766972208d891625c303f24b").content,'html.parser')

    value = soup.find('text',class_="DonutChart--innerValue--2rO41 AirQuality--extendedDialText--2AsJa").text

    quality = soup.find('span',class_="AirQualityText--severity--1fu5k AirQuality--extendedDialCategotyText--1Adwm").text

    pollution = soup.find('div',class_="AirQuality--rightCol--3MRhw").text

    quality_desc = soup.find('p',class_="AirQualityText--severityText--1wT_O AirQuality--extendedDialSeverityText--2rz1B").text

    air_quality = {
        'Value': value,
        'Quality': quality,
        'Quality_Description': quality_desc,
        'Pollution': pollution,
    }
    return dict(air_quality)

def get_weather():
    soup = BeautifulSoup(requests.get("https://weather.com/weather/today/l/10.48,107.21").content,'html.parser')

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
        'Air_Quality':get_airquality(),
    }
    
    print(weather)

    return weather

def data_prepare():
    
    if path.isfile(filename) is False:
        f =  open(filename,'a')
        f.write("[]")
        f.close()

    with open(filename) as fp:
        list_weather = json.load(fp)

    raw_data = {
        'weather': get_weather(),
        'datetime' : get_time()
    }
    list_weather.append(raw_data)

    return list_weather

def write_weather(listTemp):
    with open(filename, 'w') as json_file:
        json.dump(listTemp, json_file,indent=4,separators=(',',': '))
    
    print(listTemp.pop())

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
