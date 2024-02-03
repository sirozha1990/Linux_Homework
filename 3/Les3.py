from Task1HW1 import find_subprocess
import zlib
import yaml



with open("config.yaml") as f:
    data = yaml.safe_load(f)



def crc32(cmd):
    with open(cmd, 'rb') as g:
        hash = 0
        while True:
            s = g.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)


class Test_positiv:
    def test_step1(self, make_folders, clear_folders, make_files):
        res1 = find_subprocess(f"cd {data['tst']}; 7z a -t{data['config_type']} {data['out']}/arx2", "Everything is Ok")
        res2 = find_subprocess(f"ls {data['out']}", "")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        res = []
        res.append(find_subprocess(f"cd {data['tst']}; 7z a -t{data['config_type']} {data['out']}/arx2", "Everything is Ok"))
        res.append(find_subprocess(f"cd {data['out']}; 7z e arx2.{data['config_type']} -o{data['folder1']} -y", "Everything is Ok"))
        for item in make_files:
            res.append(find_subprocess(f"ls {data['folder1']}", item))

        assert all(res), "test2 FAIL"

    def test_step3(self):
        assert find_subprocess(f"cd {data['out']}; 7z l arx2.{data['config_type']}", f"{data['count']}")

    def test_step4(self):
        assert find_subprocess(f"cd {data['out']}; 7z t arx2.{data['config_type']}", "Everything is Ok"), "test4 FAIL"

    def test_step5(self):
        assert find_subprocess(f"cd {data['out']}; 7z d arx2.7z", "Everything is Ok"), "test5 FAIL"

    def test_step6(self):
        assert find_subprocess(f"cd {data['out']}; 7z u arx2.7z", "Everything is Ok"), "test6 FAIL"

    def test_step7(self, clear_folders, make_files):
        find_subprocess(f"cd {data['tst']}; 7z a {data['out']}/arx2", "Everything is Ok")
        assert find_subprocess(f"cd {data['out']} && 7z x arx2.7z -o{data['folder1']}", "Everything is Ok")

    def test_step8(self):
        res1 = crc32(f"{data['out']}/arx2.7z").lower()
        assert find_subprocess(f"crc32 {data['out']}/arx2.7z", res1), "test8 FAIL"