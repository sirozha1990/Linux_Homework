from checkers import checkout, getout
import yaml
from sshcheckers import ssh_checkout, upload_files

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)

class TestPositive:

    def save_log(self, start_time, name_file):
        with open(name_file, "w") as f:
            f.write(getout(f"journalctl --since '{start_time}'"))


    def test_step0(self, time_now):
        res = []
        upload_files("0.0.0.0", "user2", "11", "tests/p7zip-full.deb", "/home/user2/p7zip-full.deb")
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                                "Настраивается пакет"))
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -s p7zip-full",
                                "Status: install ok installed"))
        self.save_log(time_now, "step0")
        assert all(res)

    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        # test1
        res1 = ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
        res2 = ssh_checkout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_out"]), "arx.7z")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z e arx.7z -o{} -y".format(data["folder_out"], data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_ext"]), item))
        assert all(res)

    def test_step3(self):
        # test3
        assert ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z t arx.7z".format(data["folder_out"]), "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z u arx2.7z".format(data["folder_in"]), "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        for i in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z l arx.7z".format(data["folder_out"], data["folder_ext"]), i))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z x arx.7z -o{} -y".format(data["folder_out"], data["folder_ext2"]), "Everything is Ok"))
        for i in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_ext2"]), i))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],"ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        assert ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z d arx.7z".format(data["folder_out"]), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for i in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z h {}".format(data["folder_in"], i), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_in"], i)).upper()
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], "cd {}; 7z h {}".format(data["folder_in"], i), hash))
        assert all(res), "test8 FAIL"

    def test_step9(self, time_now):
        res = []
        upload_files("0.0.0.0", "user2", "11", "tests/p7zip-full.deb", "/home/user2/p7zip-full.deb")
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -r p7zip-full",
                                "Удаляется"))
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -s p7zip-full",
                                "Status: deinstall ok"))
        self.save_log(time_now, "step1")
        assert all(res)