from flask import Flask
import json

filename = 'data.json'

app = Flask(__name__)

@app.route('/')
def main():
    with open(filename) as fp:
        list_weather = json.load(fp)
    return {'data' :list_weather}

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)