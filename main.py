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
overwrite_users_data = False #Перезаписывает данные для всех пользователей тоесть обнуляет их

def init(): #Делаем инициализацию данных
    global users_data
    if not os.path.exists('test'):
        os.mkdir('test')    
    if not os.path.exists('users_data.json'):
        with open('users_data.json', 'w') as file:
            json.dump(dict(), file)
    with open('users_data.json', 'r') as users_data_json:
        users_data = json.load(users_data_json)
        if overwrite_users_data: #Полностью стирает все данные о пользователях и записывает заново
            for username in users_data:
                password = users_data[username]['password']
                users_data[username] = dict()
                users_data[username]['password'] = password

def save_users_data(): #Функция которая работает в фоне и каждые 15 секунд сохраняет информацию о пользователях
    while True:
        data_to_save = users_data.copy()
        with open('users_data.json', 'w') as file:
            json.dump(data_to_save, file, indent=2)
        time.sleep(15)

def login_required(func): #Декоративная функция для требования авторизации
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_func



@app.route('/')
def index():
    username = session.get('username', None)
    return render_template('index.html', username = username)

@app.route('/login', methods = ['GET', 'POST']) #Функция авторизации
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username not in users_data) or (users_data[username]['password'] != password):
            return render_template('login.html', error = 'Неправильное имя или пароль')
        else:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')


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
    if not os.path.exists('tasks/' + contest + '/' + 'condition_contest.json'):
        abort(404)
    with open('tasks/' + contest + '/' + 'condition_contest.json', 'r') as file:
        condition_contest = json.load(file)
    return render_template('contest.html',
    contest_name = condition_contest['contest_name'], contest_info = condition_contest['contest_info'],
    A_name = condition_contest.get('A_name', None), A_info = condition_contest.get('A_info', None), A_difficulty = condition_contest.get('A_difficulty', None), A_ref = condition_contest.get('A_ref', None), A_score = users_data[username].get(contest + 'A', 0),
    B_name = condition_contest.get('B_name', None), B_info = condition_contest.get('B_info', None), B_difficulty = condition_contest.get('B_difficulty', None), B_ref = condition_contest.get('B_ref', None), B_score = users_data[username].get(contest + 'B', 0),
    C_name = condition_contest.get('C_name', None), C_info = condition_contest.get('C_info', None), C_difficulty = condition_contest.get('C_difficulty', None), C_ref = condition_contest.get('C_ref', None), C_score = users_data[username].get(contest + 'C', 0),
    D_name = condition_contest.get('D_name', None), D_info = condition_contest.get('D_info', None), D_difficulty = condition_contest.get('D_difficulty', None), D_ref = condition_contest.get('D_ref', None), D_score = users_data[username].get(contest + 'D', 0),
    E_name = condition_contest.get('E_name', None), E_info = condition_contest.get('E_info', None), E_difficulty = condition_contest.get('E_difficulty', None), E_ref = condition_contest.get('E_ref', None), E_score = users_data[username].get(contest + 'E', 0)
    )

@app.route('/<contest>/<num>') #Функция для возврата страницы задачи
@login_required
def task(contest, num):
    if not os.path.exists('tasks/' + contest + '/' + num + '/' + 'condition_task.json'):
        abort(404)
    username = str(session.get('username'))
    path_condition = 'tasks/' + contest + '/' + num + '/' + 'condition_task.json'
    path_condition_long = 'tasks/' + contest + '/' + num + '/' + 'condition_task_long.txt'
    with open(path_condition, 'r') as condition:
        condition_task = json.load(condition)
    with open(path_condition_long, 'r') as condition_long:
        condition_task_long = condition_long.read() #Нужно если очень большое условие у задачи
    return render_template('task.html',
                           time_limit = condition_task.get('time_limit', ''),
                           memory_limit = condition_task.get('memory_limit', ''),
                           name = condition_task.get('name', ''),
                           condition = condition_task.get('condition', condition_task_long),
                           sample_in_1 = condition_task.get('sample_in_1', ''),
                           sample_out_1 = condition_task.get('sample_out_1', ''),
                           sample_in_2 = condition_task.get('sample_in_2', ''),
                           sample_out_2 = condition_task.get('sample_out_2', ''),
                           is_solved = users_data[username].get(contest + num, '0'),
                           contest = contest,
                           num = num
                           )

@app.route('/check', methods=['POST']) #Функция для проверки решения пользователей
@login_required
def check():
    id = uuid.uuid4() #генерирует случайны id для поссылки пользователя
    username = str(session.get('username'))
    code = str(request.form.get('code'))
    language = str(request.form.get('lang'))
    contest = str(request.form.get('contest'))
    num = str(request.form.get('num'))
    path = 'tasks/' + contest + '/' + num + '/'
    with open(f'test/{id}.{language}', 'w') as file:
        file.write(code)
    res = subprocess.run(['python3', 'checker.py'], input=f"{language}\n{path}\n{id}", text=True, capture_output=True)
    out = res.stdout
    if out.split()[0].isdigit(): #Проверка что с проверки пришли баллы а не ошибка
        users_data[username][contest + num] = max(users_data[username].get(contest + num, 0), int(out.split()[0]))
    return out




if __name__ == "__main__":
    init()
    thread = threading.Thread(target=save_users_data, daemon=True) #Запускает функцию в фоне чтобы не мешала основному коду
    thread.start()
    app.run(debug=True, host='0.0.0.0') #Если стоит дебаг то код на питоне не работает
    #host = '0.0.0.0' позваляет достучаться из локальной сети
