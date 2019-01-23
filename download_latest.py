from pathlib import Path
from utility import download_all


def main():
    # todo: make sure dirs are created if they do not exist!
    # todo: add some way to track progress, progressbar?
    current_working_directory = Path().cwd()
    base_data_dir = current_working_directory / 'data' / 'raw'
    parsed_data_dir = current_working_directory / 'data' / 'parsed'

    for source, cookies in [('uffenheim', None),
                            ('wunderground', None),
                            ('timeanddate', {'TIMEANDDATE': 'fud_1:fup_1:fut_1:fuw_1:fur_1'})]:
        download_url_generator = getattr(__import__('download_url_generator', fromlist=[source]), source)
        parsing_function = getattr(__import__('parsing', fromlist=[source]), source)

        links = download_url_generator(base_data_dir)
        download_all(inputs=links, cookies=cookies)
        parsing_function(raw_data_path=base_data_dir / source,
                         parsed_data_path=parsed_data_dir / (source + '.csv'))


if __name__ == '__main__':
    main()
