from pathlib import Path
from utility import download_all
from tqdm import tqdm


def main():
    current_working_directory = Path().cwd()
    base_data_dir = current_working_directory / 'data' / 'raw'
    parsed_data_dir = current_working_directory / 'data' / 'parsed'

    base_data_dir.mkdir(parents=True, exist_ok=True)
    parsed_data_dir.mkdir(parents=True, exist_ok=True)

    data_sources = [('uffenheim', None),
                    ('wunderground', None),
                    ('timeanddate', {'TIMEANDDATE': 'fud_1:fup_1:fut_1:fuw_1:fur_1'})]

    def download_and_parse():
        for source, cookies in data_sources:
            download_url_generator = getattr(__import__('download_url_generator', fromlist=[source]), source)
            parsing_function = getattr(__import__('parsing', fromlist=[source]), source)

            links = download_url_generator(base_data_dir / source)
            yield 'Downloading data from {}'.format(source)
            download_all(inputs=links, cookies=cookies)
            yield 'Parsing data from {}'.format(source)
            parsing_function(raw_data_path=base_data_dir / source,
                             parsed_data_path=parsed_data_dir / (source + '.csv'))
        yield 'Done!'

    progress_bar = tqdm(download_and_parse(), total=len(data_sources) * 2 + 1)
    for state in progress_bar:
        progress_bar.set_postfix(step=state)


if __name__ == '__main__':
    main()
