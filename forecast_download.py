import requests
import json
import re
import time
import os
import logging
from datetime import date
from datetime import timedelta


def main():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - [%(levelname)s] - %(message)s')

    session = requests.session()

    cookies = {'TIMEANDDATE': 'fud_1:fup_1:fut_1:fuw_1:fur_1'}

    start_date = date(2018, 3, 1)

    days_to_download = abs(start_date - date.today()).days

    for date_offset in range(0, days_to_download):
        current_date = start_date + timedelta(days=date_offset)

        date_str = '{0}{1:02d}{2:02d}'.format(current_date.year, current_date.month, current_date.day)

        file_name = '{}.json'.format(date_str)

        if file_name in os.listdir('forecasts'):
            logging.info('{} already cached'.format(date_str))
            continue

        url = 'https://www.timeanddate.com/scripts/cityajax.php?' \
              'n=@2820423&mode=historic&' \
              'hd={}&month={}&year={}&json=1'.format(date_str, current_date.month, current_date.year)

        response = session.get(url=url, cookies=cookies)

        raw_data = response.content.decode('utf-8')
        if response.status_code != 200:
            logging.critical('{} {}'.format(date_str, response.status_code))
            logging.critical('{}'.format(raw_data))
            exit(1)
        else:
            logging.info('{} {} OK'.format(date_str, response.status_code))

        with open('forecasts/{}'.format(file_name), mode='w+', encoding='utf-8') as output:

            raw_data = re.sub('([[",][,{])(.+?)([:\["])', '\g<1>"\g<2>"\g<3>', raw_data)

            json_data = json.loads(raw_data)
            output.write(json.dumps(json_data, indent=4, sort_keys=True))

        time.sleep(1)


if __name__ == '__main__':
    main()
