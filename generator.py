import random
import subprocess
import os



def compilate(): #Компилирует код на с++
    subprocess.run(['g++', f'{path}/solution.cpp', '-o', f'{path}/solution.out'])



def gen_digit(l, r): #Генерирует число в диапазоне от l
    return random.randint(l, r)



def retest(): #Делает ретесты для всех тестов без изменения тестов
    if language == 'cpp':
        compilate()
    for i in range(1, 101):
        test = path + '/test/' + str(i) + '.txt'
        ans = path + '/ans/' + str(i) + '.txt'
        with open(test, 'r') as in_file, open(ans, 'w') as out_file:
            if language == 'cpp':
                subprocess.run([f'{path}/solution.out'], stdin=in_file, stdout=out_file)
            else:
                subprocess.run(['python3', 'solution.py'], stdin=in_file, stdout=out_file)



def gen_arr(n, l, r): #Генерирует массив
    arr = [0] * n
    for i in range(n):
        arr[i] = gen_digit(l, r)
    return arr



def shuffle(arr): #Перемешивает массив
    random.shuffle(arr)
    return arr



def gen_permutation(n, start1 = False): #Генерирует перестановки start1 отвечает за отсчет с 1 если он true
    arr = [0] * n
    for i in range(n):
        arr[i] = i + start1
    shuffle(arr)
    return arr



def generate(): #Генерирует тесты и запускает их тут меняется функция для генерации
    if language == 'cpp':
        compilate()
    for i in range(1, 101):
        test = path + '/test/' + str(i) + '.txt'
        ans = path + '/ans/' + str(i) + '.txt'
        with open(test, 'w') as file:
            n = gen_digit(1, gen_digit(1, 100000)) #Вот тут должна быть нужная генерация для записи в файл
            file.write(f'{n}')
        with open(test, 'r') as in_file, open(ans, 'w') as out_file:
            if language == 'cpp':
                subprocess.run([f'{path}/solution.out'], stdin=in_file, stdout=out_file)
            else:
                subprocess.run(['python3', 'solution.py'], stdin=in_file, stdout=out_file)



path = 'tasks/contest1/A' #Путь до задачи на которую идут тесты
language = 'cpp' #Язык на котором на котором написано правильное решение ('python' | 'cpp')


generate()


if language == 'cpp': #Удаляем ненужный файл
    if os.path.exists('solution.out'):
        os.remove('solution.out')