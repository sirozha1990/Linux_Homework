import subprocess
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)
class Test_negativ:
    def find_subprocess_negativ(self, path: str, text: str):
        result = subprocess.run(path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        lst = result.stdout.split("\n") + result.stderr.split("\n")
        print(lst)
        if result.returncode != 0:
            if text in lst:
                return True
            else:
                return False
        else:
            return False



    def test_step1(self, make_bad_arx):
        assert self.find_subprocess_negativ(f"cd {data['out']}; 7z e arx2bad.7z -o{data['folder1']} -y", "Is not archive"), "test2 FAIL"
    def test_step2(self):
        assert self.find_subprocess_negativ(f"cd {data['out']}; 7z t arx2bad.7z", "Is not archive"), "test3 FAIL"