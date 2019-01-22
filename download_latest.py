from pathlib import Path
import download_url_generator
import parsing
from utility.data_download import download_all


def main():
    base_data_dir = Path().cwd() / 'data' / 'raw'
    parsed_data_dir = Path().cwd() / 'data' / 'parsed'

    uffenheim_links = download_url_generator.uffenheim(base_path=base_data_dir / 'uffenheim')
    download_all(inputs=uffenheim_links)

    wunderground_links = download_url_generator.wunderground(base_path=base_data_dir / 'wunderground')
    download_all(inputs=wunderground_links)

    timeanddate_cookies = {'TIMEANDDATE': 'fud_1:fup_1:fut_1:fuw_1:fur_1'}
    timeanddate_links = download_url_generator.timeanddate(base_path=base_data_dir / 'timeanddate')
    download_all(inputs=timeanddate_links, cookies=timeanddate_cookies)

    parsing.uffenheim(raw_data_path=base_data_dir / 'uffenheim', parsed_data_path=parsed_data_dir / 'uffenheim.csv')


if __name__ == '__main__':
    main()
