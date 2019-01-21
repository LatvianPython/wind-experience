import requests
import json
import os
import time
import logging
import csv
from datetime import datetime
from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup


def download_latest():

    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - [%(levelname)s] - %(message)s')

    url = 'https://freemeteo.co.uk/weather/uffenheim/history/daily-history/' \
          '?gid=2820423&station=3567&date={0}-{1:02d}-{2:02d}&language=english&country=germany'

    session = requests.session()

    start_date = date(2018, 3, 1)

    days_to_download = abs(start_date - date.today()).days

    for date_offset in range(0, days_to_download):
        current_date = start_date + timedelta(days=date_offset)

        date_str = '{0}{1:02d}{2:02d}'.format(current_date.year, current_date.month, current_date.day)

        file_name = '{}.json'.format(date_str)

        if file_name in os.listdir('freemeteo'):
            logging.info('{} already cached'.format(date_str))
            continue

        response = session.get(url=url.format(current_date.year, current_date.month, current_date.day))

        content = response.content.decode('utf-8')

        if response.status_code != 200:
            logging.critical('{} {}'.format(date_str, response.status_code))
            logging.critical('{}'.format(content))
            exit(1)
        else:
            logging.info('{} {} OK'.format(date_str, response.status_code))

        soup = BeautifulSoup(content, 'html.parser')

        table = soup.find('table', 'daily-history')
        headers = [th.text for th in table.select("tr th")]

        rows = [{headers[ind]: td.text for ind, td in enumerate(row.find_all("td"))} for row in table.select("tr + tr")]

        with open('freemeteo/{}'.format(file_name), mode='w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(rows, indent=4, sort_keys=True))

        time.sleep(1)


def parse_reading(reading, file_name):
    converted_reading = {}
    reading_date = datetime(int(file_name[:4]), int(file_name[4:6]), int(file_name[6:8]))

    for key in ['Pressure', 'Rel. humidity', 'Temperature', 'Time', 'Wind']:
        
        value = reading[key]

        if key == 'Pressure':
            converted_reading['pressure'] = float(value.replace('mb', ''))
        elif key == 'Rel. humidity':
            try:
                humidity = int(value.replace('%', ''))
            except ValueError:
                if len(value) == 1:
                    humidity = None
                else:
                    raise ValueError(value)
            converted_reading['humidity'] = humidity
        elif key == 'Temperature':
            converted_reading['temperature'] = int(value.replace('°C', ''))
        elif key == 'Time':
            converted_reading['time'] = str(reading_date + timedelta(hours=int(value[:2]), minutes=int(value[3:])))
        elif key == 'Wind':
            try:
                degrees_pos = value.find('°') + 1
                wind_speed = int(value[degrees_pos:value.find(' ')])
            except ValueError:
                if value == 'Calm':
                    wind_speed = 0
                elif 'Variable at ' in value:
                    try:
                        wind_speed = int(value[len('Variable at '):value.rfind(' ')])
                    except ValueError:
                        wind_speed = None
                else:
                    raise ValueError(value)

            converted_reading['wind_speed'] = wind_speed

    return converted_reading


def create_csv():
    data_dir = 'freemeteo'
    files = [file for file in os.listdir(data_dir) if 'json' in file]

    full_data_set = []

    for file in files:
        # todo: remove debug code, exit + [:1]
        with open('{}/{}'.format(data_dir, file), mode='r', encoding='utf-8') as data:
            full_data_set += [parse_reading(d, file) for d in json.loads(data.read())]

    with open('freemeteo.csv', mode='w+', encoding='utf-8', newline='') as csv_file:
        fieldnames = [column for column in full_data_set[0].keys()]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(full_data_set)


def refresh_data():
    download_latest()
    create_csv()


if __name__ == '__main__':
    create_csv()
