from pathlib import Path
import download_url_generator
import parsing
from utility.data_download import download_all


def main():
    current_working_directory = Path().cwd()
    base_data_dir = current_working_directory / 'data' / 'raw'
    parsed_data_dir = current_working_directory / 'data' / 'parsed'

    uffenheim_links = download_url_generator.uffenheim(base_path=base_data_dir / 'uffenheim')
    download_all(inputs=uffenheim_links)

    wunderground_links = download_url_generator.wunderground(base_path=base_data_dir / 'wunderground')
    download_all(inputs=wunderground_links)

    timeanddate_cookies = {'TIMEANDDATE': 'fud_1:fup_1:fut_1:fuw_1:fur_1'}
    timeanddate_links = download_url_generator.timeanddate(base_path=base_data_dir / 'timeanddate')
    download_all(inputs=timeanddate_links, cookies=timeanddate_cookies)

    parsing.timeanddate(raw_data_path=base_data_dir / 'timeanddate',
                        parsed_data_path=parsed_data_dir / 'timeanddate.csv')
    parsing.uffenheim(raw_data_path=base_data_dir / 'uffenheim',
                      parsed_data_path=parsed_data_dir / 'uffenheim.csv')


if __name__ == '__main__':
    main()
