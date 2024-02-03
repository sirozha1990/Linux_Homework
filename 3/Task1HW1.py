import subprocess
import string

def find_subprocess(path: str, text: str):
    result = subprocess.run(path, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    new_lst = result.stdout.translate(str.maketrans('', '', string.punctuation))
    print(new_lst)
    if result.returncode == 0:
        if text in new_lst:
            return True
        else:
            return False
    else:
        return False


print(find_subprocess("cat /etc/os-release", 'VERSIONID2204'))