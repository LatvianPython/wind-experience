import json
import requests
import os
import csv

# data will be saved as .json and .csv
file_name = '2018'

json_file_name = '{}.json'.format(file_name)
csv_file_name = '{}.csv'.format(file_name)

# format: yyyy-mm-dd
# how much data to request
time_frame = {'from': '2018-08-01',
              'to': '2018-08-31'}

# api link
link = 'https://www.wind-erleben.de/ajaxdata/data/all/{}/{}/'.format(time_frame['from'], time_frame['to'])


def get_data():
    # so as to not query site, if we already have the full data downloaded, use it instead
    if json_file_name not in os.listdir('.'):
        with requests.get(link) as response:
            # they send back invalid JSON, thus we just remove that part
            temp_json = json.loads(response.content.decode('utf-8').replace('"success":true,', ''))

            with open(json_file_name, mode='w', encoding='utf-8') as json_file:
                json_file.write(json.dumps(temp_json))
    else:
        with open(json_file_name, mode='r', encoding='utf-8') as json_file:
            temp_json = json.loads(json_file.read())
    return temp_json['data']['values']


if __name__ == '__main__':
    # site provides its data types only in german
    with open('translation_config.json', mode='r', encoding='utf-8') as translation_file:
        translation = json.loads(translation_file.read())

    data_set = get_data()

    main_data = {}

    for json_key, csv_key in translation.items():
        # data set is organized per data type, sometimes there is no data for a specific hour for all types
        for reading in data_set[json_key]:
            # x: date  y: value
            try:
                main_data[reading['x']][csv_key] = reading['y']
            except KeyError:
                data = {k: 0 for k in translation.values()}
                data['measurement_date'] = reading['x']
                data[csv_key] = reading['y']
                main_data[reading['x']] = data

    with open(csv_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['measurement_date'] + [k for k in translation.values()]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(main_data.values())
