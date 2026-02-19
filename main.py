from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps
import subprocess
import json
import os

app = Flask(__name__)
app.secret_key = 'qhtgyuj12cAv0.'
users_data = dict() 
overwrite_users_data = True #Перезаписывает данные для всех пользователей тоесть обнуляет их

def load_users(): #Делаем инициацию данных
    global users_data
    with open('users_data.json') as file: #Получаем данные пользователей
        users_data = json.load(file)
    for name in users_data:
        path = 'users/' + name + '.json'
        if (not os.path.exists(path)) or overwrite_users_data:
            with open(path, 'w') as file:
                json.dump(dict(), file)

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
        if (username not in users_data) or (users_data[username] != password):
            return render_template('login.html', error = 'Неправильное имя или пароль')
        else:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout', methods = ['GET', 'POST']) #Функция чтобы выйти из учетной записи
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
    

@app.route('/<contest>') #Функция для возврата страницы контеста
@login_required
def contest(contest):
    username = str(session.get('username'))
    with open('tasks/' + contest + '/' + 'condition_contest.json', 'r') as file:
        condition_contest = json.load(file)
    with open('users/' + username + '.json', 'r') as file:
        user = json.load(file)
    return render_template('contest.html',
    contest_name = condition_contest['contest_name'], contest_info = condition_contest['contest_info'],
    A = condition_contest.get('A', ''), A_info = condition_contest.get('A_info', ''), A_ref = condition_contest.get('A_ref', ''), A_score = user.get(contest + 'A', 0),
    B = condition_contest.get('B', ''), B_info = condition_contest.get('B_info', ''), B_ref = condition_contest.get('B_ref', ''), B_score = user.get(contest + 'B', 0),
    C = condition_contest.get('C', ''), C_info = condition_contest.get('C_info', ''), C_ref = condition_contest.get('C_ref', ''), C_score = user.get(contest + 'C', 0),
    D = condition_contest.get('D', ''), D_info = condition_contest.get('D_info', ''), D_ref = condition_contest.get('D_ref', ''), D_score = user.get(contest + 'D', 0),
    E = condition_contest.get('E', ''), E_info = condition_contest.get('E_info', ''), E_ref = condition_contest.get('E_ref', ''), E_score = user.get(contest + 'E', 0)
    )

@app.route('/<contest>/<num>') #Функция для возврата страницы задачи
@login_required
def task(contest, num):
    username = str(session.get('username'))
    with open('users/' + username + '.json', 'r') as file:
        user = json.load(file)
    with open('tasks/' + contest + '/' + num + '/' + 'condition_task.json', 'r') as file:
        condition_task = json.load(file)
    return render_template('task.html',
                           time_limit = condition_task.get('time_limit', ''),
                           memory_limit = condition_task.get('memory_limit', ''),
                           name = condition_task.get('name', ''),
                           condition = condition_task.get('condition', ''),
                           sample_in_1 = condition_task.get('sample_in_1', ''),
                           sample_out_1 = condition_task.get('sample_out_1', ''),
                           sample_in_2 = condition_task.get('sample_in_2', ''),
                           sample_out_2 = condition_task.get('sample_out_2', ''),
                           is_solved = user.get(contest + num, '0'),
                           contest = contest,
                           num = num
                           )

@app.route('/check', methods=['POST']) #Функция для проверки решения пользователей
@login_required
def check():
    username = str(session.get('username'))
    with open('users/' + username + '.json', 'r') as file:
        user = json.load(file)
    code = str(request.form.get('code'))
    language = str(request.form.get('lang'))
    contest = str(request.form.get('contest'))
    num = str(request.form.get('num'))
    path = 'tasks/' + contest + '/' + num + '/'
    if language == 'python':
        with open('user/code.py', 'w') as file:
            file.write(code)
            file.close()
    else:
        with open('user/code.cpp', 'w') as file:
            file.write(code)
            file.close()
    res = subprocess.run(['python3', 'checker.py'], input=f"{language}\n{path}\n", text=True, capture_output=True)
    out = res.stdout
    print(out)
    if out.split()[0].isdigit():
        user[contest + num] = max(user.get(contest + num, 0), int(out.split()[0]))
    with open('users/' + username + '.json', 'w') as file:
        print(user)
        json.dump(user, file)
    return out




if __name__ == "__main__":
    load_users()
    app.run(debug=True) #Если стоит дебаг то код на питоне не работает
