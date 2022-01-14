import datetime

import requests, json
import pandas as pd

url = 'https://www.data199.com/api/v1/device'

data = {
    'devicetoken': 'dlVmBf07TgSvo30C91JlZy:APA91bFaVNRpfuanLrDVtyNgFPbQrZTNz-Cof9qGixpWJk7xgxywwG9mMVRsyKo0dr-3FFhXKeKR7xbhgTaPCeZKxEn8lXmpTB_1x325CtG6DmeXeXCpr-slwHQi_ysaeAjhFzxg6h-6',
    'vendorid': '1c05ccaf-16db-4c40-8ab4-59cc636e1e4e',
    'phoneid': '847963711631',
    'version': '1.54',
    'build': 201,
    'executable': 'eu.mobile_alerts.weatherhub',
    'bundle': 'eu.mobile_alerts.weatherhub',
    'lang': 'pt',
    'timezoneoffset': 480,
    'usecelsius': 'true',
    'usemm': 'true',
    'speedunit': 0,
    'ccon': 'false',
    'timestamp': 1642162415,
    'requesttoken': '005462843922b432596d243f49845f88',
    'deviceid': '117E0D7623A8',
    'measurementfrom': 0,
    'measurementcount': 50
}

def saveToCSV(lastMeasurement):

    df = pd.DataFrame(lastMeasurement, index=[0])

    df.to_csv('miguelito.csv', mode='a', index=False, header=True)


if __name__ == '__main__':

    response = requests.post(url, data=data)

    lastMeasurement = json.loads(response.text)['result']['devices'][0]['measurements'][0]

    lastMeasurement['datetime'] = datetime.datetime.fromtimestamp(lastMeasurement['ts'])

    saveToCSV(lastMeasurement)

