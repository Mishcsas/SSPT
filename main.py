from flask import Flask, render_template, request
import subprocess
import time

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
    language = request.form.get('lang')
    path = request.form.get('path')
    if language == 'python':
        with open('user/code.py', 'w') as file:
            file.write(code)
            file.close()
    else:
        with open('user/code.cpp', 'w') as file:
            file.write(code)
            file.close()
    subprocess.run(['python3', 'checker.py'], input=f"{language}\n{path}\n", text=True)
    with open('user/res.txt', 'r') as file:
        return file.read()




if __name__ == "__main__":
    app.run(debug=1) #Если стоит дебаг то код на питоне не работает
