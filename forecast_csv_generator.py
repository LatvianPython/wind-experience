import json
import os
import csv
from datetime import datetime
from datetime import timedelta

data_mapping = ['time', None, 'temperature', 'weather', 'wind_speed', None, 'humidity', 'pressure']


def parse_reading(reading, file_name):
    converted_reading = {}
    reading_date = datetime(int(file_name[:4]), int(file_name[4:6]), int(file_name[6:8]))
    # quick and dirty way to do this
    # todo: rewrite this
    for i in range(0, len(data_mapping)):
        if data_mapping[i] is not None:
            converted_reading[data_mapping[i]] = reading['c'][i]['h']
            if data_mapping[i] == 'time':
                converted_reading[data_mapping[i]] = str(reading_date +
                                                         timedelta(hours=int(converted_reading[data_mapping[i]][:2])))
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
                    wind_speed = int(wind_speed[:wind_speed.find(' m/s')])
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


def main():
    data_dir = "forecasts"
    files = [file for file in os.listdir(data_dir) if 'json' in file]

    full_data_set = []

    for file in files:
        with open('{}/{}'.format(data_dir, file), mode='r', encoding='utf-8') as data:
            full_data_set += [parse_reading(d, file) for d in json.loads(data.read())]

    with open('full_weather_data.csv', mode='w+', encoding='utf-8', newline='') as csv_file:
        fieldnames = [column for column in data_mapping if column is not None]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(full_data_set)


if __name__ == '__main__':
    main()
