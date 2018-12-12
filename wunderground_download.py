import requests
import json
import os
import time
import logging
import csv
from datetime import date
from datetime import timedelta


def download_latest():

    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - [%(levelname)s] - %(message)s')

    # date format = 20180610
    url = 'https://api-ak.wunderground.com/api/606f3f6977348613/history_{}/units:metric/v:2.0/q/pws:IUFFENHE3.json'

    download_dir = 'wunderground'

    session = requests.session()

    start_date = date(2018, 3, 1)

    days_to_download = abs(start_date - date.today()).days

    for date_offset in range(0, days_to_download):
        current_date = start_date + timedelta(days=date_offset)

        date_str = '{0}{1:02d}{2:02d}'.format(current_date.year, current_date.month, current_date.day)

        file_name = '{}.json'.format(date_str)

        if file_name in os.listdir(download_dir):
            logging.info('{} already cached'.format(date_str))
            continue

        response = session.get(url=url.format(date_str))

        content = response.content.decode('utf-8')

        if response.status_code != 200:
            logging.critical('{} {}'.format(date_str, response.status_code))
            logging.critical('{}'.format(content))
            exit(1)
        else:
            logging.info('{} {} OK'.format(date_str, response.status_code))

        data = json.loads(content)

        with open('{}/{}'.format(download_dir, file_name), mode='w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(data, indent=4, sort_keys=True))

        time.sleep(1)


def create_csv():
    data_dir = 'wunderground'
    files = [file for file in os.listdir(data_dir) if 'json' in file]

    full_data_set = []

    for file in files:
        with open('{}/{}'.format(data_dir, file), mode='r', encoding='utf-8') as data:
            try:
                historic_data = json.loads(data.read())['history']['days'][0]['observations']
            except IndexError:
                continue

            [(observation.update({'iso8601': observation['date']['iso8601']}),
              observation.pop('date')) for observation in historic_data]

            full_data_set += historic_data


    with open('{}.csv'.format(data_dir), mode='w+', encoding='utf-8', newline='') as csv_file:
        fieldnames = [column for column in full_data_set[0].keys()]
        fieldnames = [fieldname for fieldname in fieldnames if 'aq' != fieldname[:2] and 'software_type' != fieldname]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(full_data_set)


if __name__ == '__main__':
    download_latest()
    create_csv()
