import subprocess


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    assert checkout("cd/home/sirozha/tst; 7z a ../out/arx2", "Everything is Ok"), "test1 FAIL"


def test_step2():
    assert checkout("cd/home/sirozha/out; 7z e arx2.7z -o/home/sirozha/folder1 -y", "Everything is Ok"), "test2 FAIL"


def test_step3():
    assert checkout("cd/home/sirozha/out; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"

def test_step4():
    assert checkout("cd /home/sirozha/out; 7z l arx2.7z", "Files read from disk: 1"), "test4 FAIL"

def test_step5():
    assert checkout("cd /home/sirozha/out; 7z x arx2.7z -o/home/sirozha/folder2 -y", "Everything is Ok"), "test5 FAIL"

def test_step6():
    assert checkout("cd /home/sirozha/tst; 7z h arx2.7z | grep -i CRC -q", ""), "test6 FAIL"
