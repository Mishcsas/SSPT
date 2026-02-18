from flask import Flask, render_template, request, session, redirect, url_for
import subprocess
import json

app = Flask(__name__)
app.secret_key = 'qhtgyuj12cAv0.'
users_data = dict() 

def load_users(): #Делаем инициацию данных
    global users_data
    with open('users_data.json') as file: #Получаем данные пользователей
        users_data = json.load(file)
    for name in users_data:
        with open('users/' + name + '.json', 'w') as file:
            json.dump(dict(), file)



@app.route('/')
def index():
    username = session.get('username', None)
    return render_template('index.html', username = username)


@app.route('/login', methods = ['GET', 'POST'])
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


@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
    


@app.route('/<contest>')
def contest(contest):
    if not('username'  in session):
        return redirect(url_for('login'))
    with open('tasks/' + contest + '/' + 'condition_contest.json', 'r') as file:
        condition_contest = json.load(file)
    return render_template('contest.html', contest_name = condition_contest['contest_name'], contest_info = condition_contest['contest_info'],
                           A = condition_contest['A'], A_info = condition_contest['A_info'], A_ref = condition_contest['A_ref']) 


@app.route('/<contest>/<num>')
def task(contest, num):
    if not('username'  in session):
        return redirect(url_for('login'))
    username = str(session.get('username'))
    with open('users/' + username + '.json', 'r') as file:
        user = json.load(file)
    with open('tasks/' + contest + '/' + num + '/' + 'condition_task.json', 'r') as file:
        condition_task = json.load(file)
    return render_template('task.html',
                           time_limit = condition_task['time_limit'],
                           memory_limit = condition_task['memory_limit'],
                           name = condition_task['name'],
                           condition = condition_task['condition'],
                           sample_in_1 = condition_task['sample_in_1'],
                           sample_out_1 = condition_task['sample_out_1'],
                           sample_in_2 = condition_task['sample_in_2'],
                           sample_out_2 = condition_task['sample_out_2'],
                           is_solved = user.get(contest + num, '0'),
                           contest = contest,
                           num = num
                           )


@app.route('/check', methods=['POST'])
def check():
    if not('username' in session):
        return redirect(url_for('login'))
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
    if out.split()[0] == '100':
        user[contest + num] = '1'
    with open('users/' + username + '.json', 'w') as file:
        print(user)
        json.dump(user, file)
    return out




if __name__ == "__main__":
    load_users()
    app.run(debug=True) #Если стоит дебаг то код на питоне не работает
