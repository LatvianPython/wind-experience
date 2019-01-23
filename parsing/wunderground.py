import json
import csv
from pathlib import Path


def parse_data(raw_data_path: Path, parsed_data_path: Path):
    fieldnames = ['humidity', 'precip', 'pressure', 'temperature', 'wind_gust_speed', 'wind_speed', 'iso8601', 'epoch']

    files = [file
             for file in raw_data_path.glob('*.json')
             if file.is_file()]

    full_data_set = []

    for file in files:
        with open(file, mode='r', encoding='utf-8') as data:
            try:
                historic_data = json.loads(data.read())['history']['days'][0]['observations']
            except IndexError:
                continue

            [(observation.update([(time_format, observation['date'][time_format])
                                  for time_format in ['iso8601', 'epoch']]),
              observation.pop('date')) for observation in historic_data]

            full_data_set += historic_data

    with open(parsed_data_path, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(full_data_set)
