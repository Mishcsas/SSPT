import subprocess
import resource
import time
import json
import os

time_limit = 1
memory_limit = 256 * 1024 * 1024
path = 'tasks/contest1/A/'
language = 'cpp'

def set_limits(): #Установка лимитов(запускает дочерний процесс перед запуском основного)
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit)) #Огранчиения на память
    resource.setrlimit(resource.RLIMIT_CPU, (time_limit + 1, time_limit + 1)) #Ограничения на время
    resource.setrlimit(resource.RLIMIT_NPROC, (3, 3)) #Ограничение на количество процессов
    os.umask(0o777) #Запрет на запись файлов
    os.environ.clear() #Очистка переменных окружения

def compilate(): #Компиляция кода
    res = subprocess.run(['g++', 'user/code.cpp', '-o', 'user/code.out'], text=True, timeout=10)
    return res.returncode

def run(i): #Запускает i тест с учетом языка ограничения на время и память
    with open(f'{path}test/{i}.txt', 'r') as input_file, open('user/out.txt', 'w') as out_file:
        start = time.time() #Стартовое время
        if language == 'python': #Если питон то сразу запустить его
            ret = subprocess.run(['python3', 'user/code.py'], stdin=input_file, stdout=out_file, preexec_fn=set_limits)
        else: #Если c++ то запускать скомпилированый файл
            ret = subprocess.run(['user/code.out'], stdin=input_file, stdout=out_file, preexec_fn=set_limits)
        end = time.time() #Конечное время
        if end - start > time_limit:
            return "TL"
        if ret.returncode != 0:
            return 'UB'
        return 0
            


def check():
    cnt = 0
    for i in range(1, 101):
        res = run(i)
        if (res != 0): #Проверка на ошибки запуска кода
            return res
        with open('user/out.txt', 'r') as user, open(f'{path}ans/{i}.txt', 'r') as ans: #Проверка на совпадение ответов
            if (user.read().strip() == ans.read().strip()): #За счет strip можно игнорировать пробелы(опасно для точных тестов)
                cnt+=1
            else:
                return cnt
    return cnt

            

def main():
    global language, path, memory_limit, time_limit
    with open(path + 'condition_task.json', 'r') as file: #Получает из файла лимитов [ограничения по времени, ограничение по памяти]
        data = json.load(file) #получает данные из файла и преобразует их в словарь
        time_limit = int(data.get('time_limit').split()[0])
        memory_limit = int(data.get('memory_limit').split()[0])
        memory_limit *= 1024 * 1024 #Перевод в байты
    if (language == 'cpp' and compilate() != 0): #Компилирует если язык c++ и сразу проверяет на ошибку компиляции
        print('Ошибка компиляции')
    else:
        res = check() #Получает результат тестов
        print(res)
        

language = input()
path = input()

main()
