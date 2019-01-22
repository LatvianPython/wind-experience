from pathlib import Path
from download import uffenheim
from download import timeanddate
from utility.data_download import download_all


def main():
    base_data_dir = Path().cwd() / 'data' / 'raw'

    uffenheim_links = uffenheim.download_links(base_path=base_data_dir / 'uffenheim')
    download_all(inputs=uffenheim_links)

    timeanddate_cookies = {'TIMEANDDATE': 'fud_1:fup_1:fut_1:fuw_1:fur_1'}
    timeanddate_links = timeanddate.download_links(base_path=base_data_dir / 'timeanddate')
    download_all(inputs=timeanddate_links, cookies=timeanddate_cookies)


if __name__ == '__main__':
    main()
