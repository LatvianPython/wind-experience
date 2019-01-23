import json
import csv
import re
from datetime import datetime
from datetime import timedelta
from pathlib import Path


def parse_data(raw_data_path: Path, parsed_data_path: Path):
    # quick and dirty way to do this
    # todo: rewrite this, i really want to rewrite, but first going to reorganize
    def parse_reading(reading, file_name):
        converted_reading = {}
        reading_date = datetime(int(file_name[:4]), int(file_name[4:6]), int(file_name[6:8]))
        for i in range(0, len(data_mapping)):
            if data_mapping[i] is not None:
                converted_reading[data_mapping[i]] = reading['c'][i]['h']
                if data_mapping[i] == 'time':
                    hours = int(converted_reading[data_mapping[i]][:2])
                    minutes = int(converted_reading[data_mapping[i]][3:5])
                    converted_reading[data_mapping[i]] = str(reading_date + timedelta(hours=hours, minutes=minutes))
                elif data_mapping[i] == 'temperature':
                    temperature = str(converted_reading[data_mapping[i]]).replace('&nbsp;', ' ')
                    temperature = int(temperature[:temperature.find(' ')])
                    converted_reading[data_mapping[i]] = temperature
                elif data_mapping[i] == 'wind_speed':
                    wind_speed = converted_reading[data_mapping[i]]
                    if wind_speed == 'N/A':
                        converted_reading[data_mapping[i]] = None
                    elif wind_speed == 'No wind':
                        converted_reading[data_mapping[i]] = 0
                    else:
                        wind_speed = int(wind_speed[:wind_speed.find(' km/h')])
                        converted_reading[data_mapping[i]] = wind_speed
                elif data_mapping[i] == 'pressure':
                    pressure = converted_reading[data_mapping[i]]
                    if pressure == 'N/A':
                        converted_reading[data_mapping[i]] = None
                    else:
                        pressure = int(pressure[:pressure.find(' ')])
                        converted_reading[data_mapping[i]] = pressure
                elif data_mapping[i] == 'humidity':
                    humidity = converted_reading[data_mapping[i]]
                    if humidity == 'N/A':
                        converted_reading[data_mapping[i]] = None
                    else:
                        humidity = int(humidity[:humidity.find('%')])
                        converted_reading[data_mapping[i]] = humidity

        return converted_reading

    data_mapping = ['time', None, 'temperature', 'weather', 'wind_speed', None, 'humidity', 'pressure']

    full_data_set = []

    files = [file
             for file in raw_data_path.glob('*.json')
             if file.is_file()]

    for file in files:
        with open(file, mode='r', encoding='utf-8') as data:
            raw_data = data.read()
            raw_data = re.sub('([[",][,{])(.+?)([:\["])', '\g<1>"\g<2>"\g<3>', raw_data)
            full_data_set += [parse_reading(d, file.stem) for d in json.loads(raw_data)]

    with open(parsed_data_path, mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = [column for column in data_mapping if column is not None]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(full_data_set)
