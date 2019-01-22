from pathlib import Path
from utility.data_download import next_date


def download_links(base_path):
    base_url = 'https://www.wind-erleben.de/ajaxdata/data/all/{0}/{0}/'
    inputs = [
        (Path(base_path, '{}.json'.format(formatted_date)),
         base_url.format(formatted_date))
        for formatted_date in (current_date.strftime('%Y-%m-%d')
                               for current_date in next_date())
    ]
    return inputs
