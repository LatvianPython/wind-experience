from pathlib import Path
from utility.data_download import next_date


def download_links(base_path):
    base_url = 'https://api-ak.wunderground.com/api/606f3f6977348613/history_{}/units:metric/v:2.0/q/pws:{}.json'
    weather_station = 'IUFFENHE3'
    inputs = [
        (Path(base_path, '{}.json'.format(formatted_date)),
         base_url.format(formatted_date, weather_station))
        for formatted_date in (current_date.strftime('%Y%m%d')
                               for current_date in next_date())
    ]
    return inputs
