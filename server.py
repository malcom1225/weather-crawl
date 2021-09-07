from flask import Flask
import json

filename = 'data.json'
with open(filename) as fp:
    list_weather = json.load(fp)



server = Flask(__name__)

@server.route('/')
def index():
    return {'data' :list_weather}

@server.route('/lastest')
def lastest():
    last_data = list_weather.pop()
    
    lastmessage = f'''
    <h1>Last Weather Data at {last_data["Time"]} on {last_data["Date"]}</h1>
    <h3>Temperature : {last_data["Temperature"]} °C</h3>
    <h3>Condition : {last_data["Condition"]}</h3>
    <h3>Humidity : {last_data["Humidity"]}</h3>
    <h3>Quality: {last_data["Quality"]}</h3>
    <h3>Pollution : {last_data["Pollution"].split(':')[1]}, Value : {last_data["Pollution_Value"]}</h3>
    <h3>{last_data["Quality_Description"]}</h3>
    <h3>UV_Index : {last_data["UV_Index"]}</h3>
    '''

    return lastmessage

if __name__ == '__main__':
    server.run(debug=True,host='0.0.0.0', port=80)
    