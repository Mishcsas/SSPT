import subprocess
import resource
import time

time_limit = 1
memory_limit = 256 * 1024 * 1024
path = ''
language = 'c++'

def set_limits():
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))

def compilate():
    with open('user/error.txt', 'w') as error_file:
        res = subprocess.run(['g++', 'user/code.cpp', '-o', 'user/code.out'], stderr=error_file, text=True)
        return res.returncode

def run(i):
    with open(f'{path}test/{i}.txt', 'r') as input_file, open('user/out.txt', 'w') as out_file, open('user/error.txt', 'w') as error_file:
        try:
            start = time.time()
            if language == 'python':
                ret = subprocess.run(['python3', 'user/code.py'], stdin=input_file, stdout=out_file, stderr=error_file, timeout=max(2, time_limit), preexec_fn=set_limits)
            else:
                ret = subprocess.run(['user/code.out'], stdin=input_file, stdout=out_file, stderr=error_file, timeout=max(2, time_limit), preexec_fn=set_limits)
            end = time.time()
            if end - start > time_limit:
                return "TL"
            if ret.returncode != 0:
                return 'UB'
            return 0
        except subprocess.TimeoutExpired:
            return 'TL'


def check():
    cnt = 0
    for i in range(1, 101):
        res = run(i)
        if (res != 0):
            print(res)
            return res
        with open('user/out.txt', 'r') as user, open(f'{path}ans/{i}.txt', 'r') as ans:
            if (user.read() == ans.read()):
                cnt+=1
            else:
                with open(f'{path}test/{i}.txt', 'r') as file:
                    return 'Неправильный ответ на тесте:\n' + file.read()
    return cnt

            

def main():
    global language, path, memory_limit, time_limit
    with open('user/task.txt', 'r') as file:
        language = file.readline().strip()
        path = file.readline().strip()
        memory_limit = int(file.readline().strip())
        time_limit = int(file.readline().strip())
    if (language == 'c++' and compilate() != 0):
        with open('user/res.txt', 'w') as file:
            file.write('Ошибка компиляции')
    else:
        with open('user/res.txt', 'w', encoding="utf-8") as file:
            res = check()
            print(res)
            file.write(str(res))


main()
