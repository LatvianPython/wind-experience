from pathlib import Path
from utility.data_download import next_date


def download_links(base_path):

    base_url = 'https://www.wind-erleben.de/ajaxdata/data/all/{0}/{0}/'
    inputs = [(Path(base_path, '{}.json'.format(file)), base_url.format(file))
              for file in (ayy.strftime('%Y-%m-%d') for ayy in next_date())]

    return inputs
