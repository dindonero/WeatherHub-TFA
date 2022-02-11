import datetime
import json
import threading
import time

import pandas as pd
import requests
from flask import Flask, send_file
from os.path import exists


hours = 2.5

deviceIds = '117E0D7623A8'  # string divided by commas

url = 'https://www.data199.com/api/pv1/device/lastmeasurement'

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
}

app = Flask(__name__)

lastRunAt = 'Unknown'


@app.route("/")
def welcome_page():
    return "&nbsp" \
           "<h3>Last Request At: " + lastRunAt + "</h3>" \
           "<ol><li><a href='/ver'>Ver Log</a></li>" \
           "<li><a href='/download'>Download Log</a></li></ol>" \


@app.route("/ver")
def ver_log():
    f = open('miguelito.csv', 'r')
    logs = f.readlines()
    f.close()
    return str('<p>' + '</p><p>'.join(logs) + '</p>')


@app.route("/download")
def download_log():
    return send_file('miguelito.csv', as_attachment=True,
                     download_name='WeatherHubLog_' + str(datetime.datetime.now()) + '.csv')


def request_measure():
    global lastRunAt
    while True:
        response = requests.post(url, data='deviceids=' + deviceIds, headers=headers)

        lastMeasurement = json.loads(response.text)['devices'][0]['measurement']

        lastMeasurement['datetime'] = datetime.datetime.fromtimestamp(lastMeasurement['ts'])

        saveToCSV(lastMeasurement)

        print('Read measure at ' + str(datetime.datetime.fromtimestamp(lastMeasurement['ts'])))

        lastRunAt = str(datetime.datetime.now())

        time.sleep(hours * 60 * 60)


def saveToCSV(lastMeasurement):
    df = pd.DataFrame(lastMeasurement, index=[0])

    df.to_csv('miguelito.csv', mode='a', index=False, header=(not exists('miguelito.csv')))  # if exists skip headers

if __name__ == '__main__':
    bot = threading.Thread(target=request_measure)
    bot.start()
    app.run(host='0.0.0.0', port=80, debug=False)
    bot.join()
