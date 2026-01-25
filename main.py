from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def get_user():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    code = request.form.get('code')
    with open('user/task.txt', 'r') as task_file:
        language = task_file.readline().strip()
    if language == 'python':
        with open('user/code.py', 'w') as file:
            file.write(code)
    else:
        with open('user/code.cpp', 'w') as file:
            file.write(code)

    subprocess.run(['python3', 'checker.py'])

    with open('user/res.txt', 'r') as file:
        return file.read()




if __name__ == "__main__":
    app.run(debug=True)
