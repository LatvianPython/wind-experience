import csv
import json
from pathlib import Path

# site provides its data types only in german, here are the translations
translation = {
    '20': 'solar_generation_kw',
    '21': 'power_use_kw',
    '26': 'wind_generation_kw',
    '27': 'wind_direction_degrees',
    '28': 'wind_speed_m_s',
    '29': 'pitch_degrees',
    '30': 'rotor_speed_rpm',
    '31': 'rotation_gondola_degrees',
    '32': 'charging_station_w',
    '33': 'battery_drain_or_load_w',
    '34': 'state_of_charge_percent',
    '35': 'battery_voltage_v',
    '36': 'rlm_solar_kw',
    '37': 'slp_solar_kw',
    '38': 'chp_kw',
    '39': 'electricity_purchase_kw',
    '40': 'power_backfeed_kw',
    '41': 'total_production_kw',
    '42': 'reference_kw'
}

@profile
def parse_data(raw_data_path: Path, parsed_data_path: Path):
    files = [file
             for file in raw_data_path.glob('*.json')
             if file.is_file()]

    readings = {}

    for file in files:
        with open(file, mode='r', encoding='utf-8') as json_file:
            data_set = json.loads(json_file.read())['data']['values']

        if len(data_set) < 4:  # some days don't even have enough measurements in them, sad
            continue

        for json_key, csv_key in translation.items():
            for reading in data_set[json_key]:
                # x: date  y: value
                try:
                    readings[reading['x']][csv_key] = reading['y']
                except KeyError:
                    new_reading = {k: 0 for k in translation.values()}
                    new_reading['measurement_date'] = reading['x']
                    new_reading[csv_key] = reading['y']
                    readings[reading['x']] = new_reading

    with open(parsed_data_path, mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['measurement_date'] + list(translation.values())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')

        writer.writeheader()
        writer.writerows(readings.values())
