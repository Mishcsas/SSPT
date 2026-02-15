import subprocess
import resource
import time

time_limit = 1
memory_limit = 256 * 1024 * 1024
path = 'tasks/contest1/A/'
language = 'cpp'

def set_limits(): #Установка лимита на время
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))

def compilate(): #Компиляция кода
    with open('user/error.txt', 'w') as error_file:
        res = subprocess.run(['g++', 'user/code.cpp', '-o', 'user/code.out'], stderr=error_file, text=True)
        return res.returncode

def run(i): #Запускает i тест с учетом языка ограничения на время и память
    with open(f'{path}test/{i}.txt', 'r') as input_file, open('user/out.txt', 'w') as out_file, open('user/error.txt', 'w') as error_file:
        try:
            start = time.time() #Стартовое время
            if language == 'python': #Если питон то сразу запустить его
                ret = subprocess.run(['python3', 'user/code.py'], stdin=input_file, stdout=out_file, stderr=error_file, timeout=max(2, time_limit), preexec_fn=set_limits)
            else: #Если c++ то запускать скомпилированый файл
                ret = subprocess.run(['user/code.out'], stdin=input_file, stdout=out_file, stderr=error_file, timeout=max(2, time_limit), preexec_fn=set_limits)
            end = time.time() #Конечное время
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
        if (res != 0): #Проверка на ошибки запуска кода
            print(res)
            return res
        with open('user/out.txt', 'r') as user, open(f'{path}ans/{i}.txt', 'r') as ans: #Проверка на совпадение ответов
            if (user.read() == ans.read()):
                cnt+=1
            else:
                with open(f'{path}test/{i}.txt', 'r') as file:
                    return 'Неправильный ответ на тесте:\n' + file.read()
    return cnt

            

def main():
    global language, path, memory_limit, time_limit
    with open(path + 'limits.txt', 'r') as file: #Получает из файла лимитов [ограничения по времени, ограничение по памяти]
        time_limit = int(file.readline().strip())
        memory_limit = int(file.readline().strip())
    if (language == 'cpp' and compilate() != 0): #Компилирует если язык c++ и сразу проверяет на ошибку компиляции
        with open('user/res.txt', 'w') as file:
            file.write('Ошибка компиляции')
    else:
        with open('user/res.txt', 'w') as file: #Открывает файл и записывает в него результат тестов
            res = check()
            print(res)
            file.write(str(res))

language = input()
path = input()

main()
