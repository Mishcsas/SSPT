import json
import os



if not os.path.exists('users_data.json'): #Проверяет есть ли users_data.json если нет то создает
        with open('users_data.json', 'w') as file:
            json.dump(dict(), file, indent=2)
with open('users_data.json', 'r') as users_data_json:
    try: #Обрабатываем что он пустой
        users_data = json.load(users_data_json)
    except Exception as e:
        users_data = dict()
users_data_json.close()



print("Скрипт работает")



while True:
    string = input().split()
    username = None
    password = None
    if (len(string) >= 3):
        password = string[2]
    if (len(string) >= 2):
        username = string[1]
    command = string[0]
    if command == 'add': #Добавить пользователя
        if username == None or password == None:
            print('Синтаксическая ошибка')
            continue
        if username in users_data:
            print('Пользователь уже был')
            continue
        users_data[username] = dict()
        users_data[username]['password'] = password
        print('Успешно')
    elif command == 'del': #Удалить пользователя
        if username == None:
            print('Синтаксическая ошибка')
            continue
        if username not in users_data:
            print('Пользователя нет')
            continue
        users_data.pop(username)
        print('Успешно')
    elif command == 'clear': #Очистить задачи пользователя
        if username == None:
            print('Синтаксическая ошибка')
            continue
        if username not in users_data:
            print('Пользователя нет')
            continue
        password = users_data[username]['password']
        users_data[username].clear()
        users_data[username]['password'] = password
        print('Успешно')
    elif command == 'delall': #Удалить всех пользователей
        users_data = dict()
    elif command == 'clearall': #Очистить задачи всех пользователей
        for username in users_data:
            if username not in users_data:
                continue
            password = users_data[username]['password']
            users_data[username].clear()
            users_data[username]['password'] = password
        print('Успешно')
    elif command == 'top': #Вывести топ участников
        result = list()
        for username in users_data:
            cur_cnt = 0
            for task in users_data[username]:
                if task == 'password':
                    continue
                cur_cnt += users_data[username][task]
            result.append((cur_cnt, username))
        result.sort(reverse=True)
        with open('top.txt', 'w') as file:
            for i in range(len(result)):
                file.write(f'{i + 1}. {result[i][0]} {result[i][1]} \n')
        print('Успешно')
    elif command == 'end': #Завершить цикл
        print('Успешно')
        break
    else: #Неизвестная команда
        print('Неизвестная команда')
    with open('users_data.json', 'w') as users_data_json:
        json.dump(users_data, users_data_json, indent=2)
    users_data_json.close()