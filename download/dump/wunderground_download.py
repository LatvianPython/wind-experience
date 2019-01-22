import requests
import json
import os
import time
import random
import logging
import csv
from datetime import date
from datetime import timedelta
import multiprocessing
from joblib import delayed
from joblib import Parallel


def download_latest(station, download_dir):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    existing_files = os.listdir(download_dir)

    def download_single_day(date_str):
        thread_nr = multiprocessing.current_process().name
        thread_nr = thread_nr[thread_nr.rfind('-') + 1:]
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s] - [%(levelname)s] - thread:{:2} - %(message)s'.format(thread_nr))

        file_name = '{}.json'.format(date_str)

        try:
            response = session.get(url=url.format(date_str, station))
        except TimeoutError:
            logging.critical('Timeout Error')
            return

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

        time.sleep(random.uniform(1, 2))

    # date format = 20180610
    url = 'https://api-ak.wunderground.com/api/606f3f6977348613/history_{}/units:metric/v:2.0/q/pws:{}.json'

    session = requests.session()

    start_date = date(2018, 3, 1)

    days_to_download = abs(start_date - date.today()).days

    inputs = [file for file in [(start_date + timedelta(days=date_offset)).strftime('%Y%m%d')
              for date_offset in range(0, days_to_download)] if file + '.json' not in existing_files]

    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(download_single_day)(j) for j in inputs)


def create_csv(fieldnames, download_dir, csv_filename):
    files = [file for file in os.listdir(download_dir) if 'json' in file]

    full_data_set = []

    for file in files:
        with open('{}/{}'.format(download_dir, file), mode='r', encoding='utf-8') as data:
            try:
                historic_data = json.loads(data.read())['history']['days'][0]['observations']
            except IndexError:
                continue

            [(observation.update([(time_format, observation['date'][time_format])
                                  for time_format in ['iso8601', 'epoch']]),
              observation.pop('date')) for observation in historic_data]

            full_data_set += historic_data

    with open('{}.csv'.format(csv_filename), mode='w+', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(full_data_set)


if __name__ == '__main__':
    weather_station = 'IUFFENHE3'
    download_directory = 'wunderground/{}'.format(weather_station.lower())
    columns = ['humidity', 'precip', 'pressure', 'temperature', 'wind_gust_speed', 'wind_speed', 'iso8601', 'epoch']

    download_latest(weather_station, download_directory)
    create_csv(columns, download_directory, weather_station.lower())
