from pathlib import Path
from utility import next_date


def download_links(base_path):
    base_url = 'https://www.timeanddate.com/scripts/cityajax.php?n=@2820423&mode=historic&hd={}&month={}&year={}&json=1'
    inputs = [
        (Path(base_path, '{}.json'.format(formatted_date)),
         base_url.format(formatted_date, current_date.month, current_date.year))
        for current_date, formatted_date in ((current_date, current_date.strftime('%Y%m%d'))
                                             for current_date in next_date())
    ]
    return inputs
