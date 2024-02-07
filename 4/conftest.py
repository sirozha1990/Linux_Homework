import pytest
from checkers import checkout
import random, string
import yaml
from datetime import datetime
from sshcheckers import ssh_checkout, ssh_getout, upload_files

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)

@pytest.fixture()
def make_folders():
    return ssh_checkout(data['host'], data['user'], data['passwd'], "mkdir {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")

@pytest.fixture()
def clear_folders():
    return ssh_checkout(data['host'], data['user'], data['passwd'], "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")
@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files

@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername, testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename

@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))

@pytest.fixture()
def time_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")