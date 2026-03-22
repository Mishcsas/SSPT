from flask import Flask, render_template, request, session, redirect, url_for, abort
from functools import wraps
import subprocess
import json
import os
import uuid
import threading
import time



app = Flask(__name__)
app.secret_key = 'qhtgyuj12cAv0.'
users_data = dict()



def init(): #Делаем инициализацию данных
    global users_data
    if not os.path.exists('test'):
        os.mkdir('test')
    if not os.path.exists('users_data.json'):
        with open('users_data.json', 'w') as file:
            json.dump(dict(), file, indent=2)
    with open('users_data.json', 'r') as users_data_json: #Получаем информацию о пользователях
        try: #Обрабатываем что он пустой
            users_data = json.load(users_data_json)
        except Exception as e:
            users_data = dict()
    thread = threading.Thread(target=save_users_data, daemon=True) #Запускает функцию в фоне чтобы не мешала основному коду
    thread.start()



def save_users_data(): #Функция которая работает в фоне и каждые 15 секунд сохраняет информацию о пользователях
    while True:
        data_to_save = users_data.copy()
        with open('users_data.json', 'w') as file:
            json.dump(data_to_save, file, indent=2)
        time.sleep(15)



def login_required(func): #Декоративная функция для требования авторизации
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if 'username' not in session or session.get('username', None) not in users_data:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_func



@app.route('/')
def index():
    username = session.get('username', None)
    if (username not in users_data): #Если есть в сесии пользователя но не зареган то убираем
        session.pop('username', None)
        username = None
    return render_template('index.html', username = username)



@app.route('/login', methods = ['GET', 'POST']) #Функция авторизации
def login():
    if request.method == 'POST': #Если запрос отправки данные обрабатываем
        username = request.form.get('username')
        password = request.form.get('password')
        if (username not in users_data) or (users_data[username]['password'] != password):
            return render_template('login.html', error = 'Неправильное имя или пароль')
        else:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html') #Если запрос получения просто возвращаем страничку



@app.route('/logout', methods = ['GET', 'POST']) #Функция чтобы выйти из учетной записи
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))



@app.errorhandler(404) #Функция для обработки ошибки 404
def page_not_found(error):
    return render_template('404.html')



@app.route('/<contest>') #Функция для возврата страницы контеста
@login_required
def contest(contest):
    username = str(session.get('username'))
    path_config = 'tasks/' + contest + '/' + 'config.json'
    if not os.path.exists(path_config): #Проверяем есть ли такой конфиг если нет возвращаем 404
        abort(404)
    with open(path_config, 'r') as file:
        config = json.load(file)
    return render_template('contest.html',
    contest_name = config['contest_name'], contest_info = config['contest_info'],
    A_name = config.get('A_name', None), A_info = config.get('A_info', None), A_difficulty = config.get('A_difficulty', None), A_ref = f'/{contest}/A', A_score = users_data[username].get(contest + 'A', 0),
    B_name = config.get('B_name', None), B_info = config.get('B_info', None), B_difficulty = config.get('B_difficulty', None), B_ref = f'/{contest}/B', B_score = users_data[username].get(contest + 'B', 0),
    C_name = config.get('C_name', None), C_info = config.get('C_info', None), C_difficulty = config.get('C_difficulty', None), C_ref = f'/{contest}/C', C_score = users_data[username].get(contest + 'C', 0),
    D_name = config.get('D_name', None), D_info = config.get('D_info', None), D_difficulty = config.get('D_difficulty', None), D_ref = f'/{contest}/D', D_score = users_data[username].get(contest + 'D', 0),
    E_name = config.get('E_name', None), E_info = config.get('E_info', None), E_difficulty = config.get('E_difficulty', None), E_ref = f'/{contest}/E', E_score = users_data[username].get(contest + 'E', 0)
    )



@app.route('/<contest>/<number>') #Функция для возврата страницы задачи
@login_required
def task(contest, number):
    username = str(session.get('username'))
    path_config = 'tasks/' + contest + '/' + number + '/' + 'config.json'
    path_problem = 'tasks/' + contest + '/' + number + '/' + 'problem.txt'
    if not os.path.exists(path_config) or not os.path.exists(path_config): #Проверяем есть ли такой конфиг и проблема задачи если нет возвращаем 404
        abort(404)
    with open(path_config, 'r') as config_file:
        config = json.load(config_file)
    with open(path_problem, 'r') as problem_file:
        problem = problem_file.read()
    return render_template('task.html',
        time_limit = config.get('time_limit', ''),
        memory_limit = config.get('memory_limit', ''),
        name = config.get('name', ''),
        condition = problem,
        sample_in_1 = config.get('sample_in_1', ''),
        sample_out_1 = config.get('sample_out_1', ''),
        sample_in_2 = config.get('sample_in_2', ''),
        sample_out_2 = config.get('sample_out_2', ''),
        is_solved = users_data[username].get(contest + number, '0'),
        contest = contest,
        number = number
    )



@app.route('/check', methods=['POST']) #Функция для проверки решения пользователей
@login_required
def check():
    id = uuid.uuid4() #генерирует случайны id для поссылки пользователя
    username = str(session.get('username'))
    code = str(request.form.get('code'))
    language = str(request.form.get('lang'))
    contest = str(request.form.get('contest'))
    number = str(request.form.get('number'))
    path = 'tasks/' + contest + '/' + number + '/'
    with open(f'test/{id}.{language}', 'w') as file:
        file.write(code)
    res = subprocess.run(['python3', 'checker.py'], input=f"{language}\n{path}\n{id}", text=True, capture_output=True)
    if res.returncode != 0: #Проверяем на ошибку тестирующую систему
        return f'{res.stdout}Ошибка тестирующей системы'
    out = res.stdout
    if out.split()[0].isdigit(): #Проверка что с проверки пришли баллы а не ошибка
        users_data[username][contest + number] = max(users_data[username].get(contest + number, 0), int(out.split()[0]))
    return out



if __name__ == "__main__":
    init()
    app.run(debug=False, host='0.0.0.0') #Если стоит дебаг то код на питоне не работает
    #host = '0.0.0.0' позваляет достучаться из локальной сети
