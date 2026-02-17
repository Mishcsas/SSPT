from flask import Flask, render_template, request
import subprocess
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<contest>')
def contest(contest):
    return render_template(f'{contest}.html') 

@app.route('/<contest>/<num>')
def task(contest, num):
    print(contest)
    return render_template(f'{contest + num}.html') 


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
    res = subprocess.run(['python3', 'checker.py'], input=f"{language}\n{path}\n", text=True, capture_output=True)
    out = res.stdout
    print(out)
    return out




if __name__ == "__main__":
    app.run(debug=1) #Если стоит дебаг то код на питоне не работает
