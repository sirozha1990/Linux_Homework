import pytest
from Task1HW1 import find_subprocess

import yaml
import random
import string
import logging

with open("config.yaml") as f:
    data = yaml.safe_load(f)

logging.basicConfig(filename="stat.txt", level=logging.INFO, format='%(asctime)s %(message)s')

@pytest.fixture()
def make_folders():
    logging.info('Создание папок')
    find_subprocess(f"mkdir {data['tst']} {data['out']} {data['folder1']}", "")


@pytest.fixture()
def clear_folders():
    find_subprocess(f"rm -rf {data['tst']}/* {data['out']}/* {data['folder1']}/*", "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data['count']):
        file_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        find_subprocess(f"cd {data['tst']}; dd if=/dev/urandom of={file_name} count=1 iflag=fullblock", "")
        list_of_files.append(file_name)
    logging.info(f" make files {data['count']}, size files - {data['size']}")

    return list_of_files


@pytest.fixture()
def make_bad_arx():
    find_subprocess(f"cd {data['tst']}; 7z a {data['out']}/arx2", "Everything is Ok")
    find_subprocess(f"truncate -s 1 {data['out']}/arx2bad.7z", "")