from pathlib import Path
from download import uffenheim
from utility.data_download import download_all


def main():
    base_data_dir = Path().cwd() / 'data' / 'raw'

    uffenheim_links = uffenheim.download_links(base_data_dir / 'uffenheim')
    download_all(uffenheim_links)


if __name__ == '__main__':
    main()
