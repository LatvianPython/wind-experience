from datetime import date
from datetime import timedelta
from pathlib import Path


def download_links(base_path):
    def next_date():
        start_date = date(2018, 3, 1)
        days_to_download = abs(start_date - date.today()).days
        for date_offset in range(days_to_download):
            yield start_date.strftime('%Y-%m-%d')
            start_date = start_date + timedelta(days=1)

    base_url = 'https://www.wind-erleben.de/ajaxdata/data/all/{0}/{0}/'
    inputs = [(Path(base_path, '{}.json'.format(file)), base_url.format(file))
              for file in next_date()]

    return inputs
