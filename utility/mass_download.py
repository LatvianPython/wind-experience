import logging
import random
import time
import requests
import multiprocessing
import pathlib
from typing import List, Tuple
from joblib import delayed
from joblib import Parallel

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def download_all(inputs: List[Tuple[pathlib.Path, str]]):
    session = requests.session()

    def download_single_link(file_path: pathlib.Path, url):
        thread_nr = multiprocessing.current_process().name
        thread_nr = thread_nr[thread_nr.rfind('-') + 1:]

        file_name = file_path.stem
        if file_path.is_file():
            logger.info('{} {} already exists'.format(thread_nr, file_name))
            return

        try:
            response = session.get(url=url)
        except TimeoutError:
            logger.critical('{} Timeout Error'.format(thread_nr))
            return

        content = response.content.decode('utf-8')

        if response.status_code != 200:
            logger.critical('{} {}'.format(thread_nr, url, response.status_code))
            logger.critical('{}'.format(thread_nr, content))
            return
        else:
            logger.info('{} {} {} OK'.format(thread_nr, file_name, response.status_code))

        with open(str(file_path), mode='w', encoding='utf-8') as output_file:
            output_file.write(content)

        time.sleep(random.uniform(1, 2))

    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(download_single_link)(*j) for j in inputs)
