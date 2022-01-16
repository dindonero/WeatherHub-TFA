import datetime
import time

import requests, json
import pandas as pd

hours = 2.5

url = 'https://www.data199.com/api/pv1/device/lastmeasurement'

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
}


def saveToCSV(lastMeasurement):

    df = pd.DataFrame(lastMeasurement, index=[0])

    df.to_csv('miguelito.csv', mode='a', index=False, header=False)


if __name__ == '__main__':

    while True:

        response = requests.post(url, data='deviceids=117E0D7623A8', headers=headers)

        print(response.text)
        lastMeasurement = json.loads(response.text)['devices'][0]['measurement']

        lastMeasurement['datetime'] = datetime.datetime.fromtimestamp(lastMeasurement['ts'])

        saveToCSV(lastMeasurement)

        print('Read measure at ' + str(datetime.datetime.fromtimestamp(lastMeasurement['ts'])))

        time.sleep(hours*60*60)
