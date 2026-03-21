import subprocess
import resource
import time
import json
import os

time_limit = 1
memory_limit = 256 * 1024 * 1024
path = 'tasks/contest1/A/'
language = 'cpp'
use_checker = False
id = '1'
independent_tests = False



def set_limits(): #Установка лимитов(запускает дочерний процесс перед запуском основного)
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit)) #Огранчиения на память
    resource.setrlimit(resource.RLIMIT_CPU, (time_limit + 1, time_limit + 1)) #Ограничения на время + 1 чтобы не было ошибок
    resource.setrlimit(resource.RLIMIT_NPROC, (3, 3)) #Ограничение на количество процессов
    os.umask(0o777) #Запрет на запись файлов
    os.environ.clear() #Очистка переменных окружения



def compilate(): #Компиляция кода
    result_compilate = subprocess.run(['g++', f'test/{id}.cpp', '-o', f'test/{id}.out'], text=True, capture_output=True)
    if result_compilate.returncode != 0:
        return result_compilate.stderr
    else:
        return 0



def run(i): #Запускает i тест с учетом языка ограничения на время и память
    with open(f'{path}test/{i}.txt', 'r') as input_file, open(f'test/{id}_out.txt', 'w') as out_file:
        start = time.time()
        if language == 'py': #Если питон то сразу запустить его
            ret = subprocess.run(['python3', f'test/{id}.py'], stdin=input_file, preexec_fn=set_limits, text=True, capture_output=True)
        else: #Если c++ то запускать скомпилированый файл
            ret = subprocess.run([f'test/{id}.out'], stdin=input_file, preexec_fn=set_limits, text=True, capture_output=True)
        end = time.time()
        out_file.write(ret.stdout)
        if end - start > time_limit: #Проверяем на превышение времени
            return "Time limit exceeded"
        if ret.returncode != 0: #Возвращаем ошибку
            return ret.stderr
        return 0



def run_checker(): #Запускает чекер для определенной задачи и записывает его результат в файл
    with open(f'test/{id}_out.txt', 'r') as file: #Открываем файл пользователя и обрабатываем его нашим чекером
        res = subprocess.run(['python3', f'{path}checker.py'], stdin=file, text=True, capture_output=True)
    with open(f'test/{id}_out.txt', 'w') as file: #Записываем в файл пользователя результат обработки чекером
        file.write(res.stdout)



def check(): #Функция для проверки решения пользователя
    cnt = 0
    for i in range(1, 101):
        result_run = run(i)
        if (result_run != 0): #Проверка на ошибки запуска кода
            return result_run
        if use_checker:
            run_checker()
        with open(f'test/{id}_out.txt', 'r') as user, open(f'{path}ans/{i}.txt', 'r') as ans: #Проверка на совпадение ответов
            if (user.read().strip() == ans.read().strip()):
                cnt+=1
            else:
                if not independent_tests: #Проверяем если у нас не независимые тесты то прерываемся при первой ошибке
                    return cnt
    return cnt



def main(): #Получает данные по задаче и запускает проверку
    global language, path, memory_limit, time_limit, use_checker, independent_tests
    path_config = path + 'config.json'
    if not os.path.exists(path_config): #Проверяем есть ли данные по задаче если нет то запишем пустой словарь
        with open(path_config, 'w') as file:
            json.dump(dict(), file, indent=2)
    with open(path_config, 'r') as file: #Получает данные из файла задачи
        data = json.load(file)
        time_limit = int(data.get('time_limit', '1').split()[0]) #Возвращаем 1 секунду если нам не дали время
        memory_limit = int(data.get('memory_limit', '256').split()[0]) #Возвращаем 256 мб если нам не дали память
        use_checker = data.get('use_checker', False)
        independent_tests = data.get('independent_tests', False)
        memory_limit *= 1024 * 1024 #Перевод в байты
    if (language == 'cpp'): #Компилирует если язык c++ и сразу проверяет на ошибку компиляции
        result_compilate = compilate()
        if result_compilate != 0:
            print(result_compilate)
            os.remove(f'test/{id}.{language}')
            return 0
    result_check = check() #Получает результат тестов
    os.remove(f'test/{id}.{language}')
    os.remove(f'test/{id}_out.txt')
    if language == 'cpp':
        os.remove(f'test/{id}.out')
    print(result_check)
        

language = input() #Язык програмирования
path = input() #Путь до задачи
id = input() #Айди текущего кода чтобы была возможность асинхроности

main()
