import subprocess

def execute_command(command, text):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        if text in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        return False


command = "ls"
text = "file.txt"
result = execute_command(command, text)
print(result)  # Выведет True, если в текущей директории есть файл file.txt
