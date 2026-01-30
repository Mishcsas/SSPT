import random
import subprocess

def compilate():
    subprocess.run(['g++', f'{path}/solution.cpp', '-o', f'{path}/solution.out'])

def gen_digit(l, r):
    return random.randint(l, r)

def retest():
    for i in range(1, 101):
        test = path + '/test/' + str(i) + '.txt'
        ans = path + '/ans/' + str(i) + '.txt'
        with open(test, 'r') as in_file, open(ans, 'w') as out_file:
            subprocess.run([f'{path}/solution.out'], stdin=in_file, stdout=out_file)

def generate():
    compilate()
    for i in range(1, 101):
        test = path + '/test/' + str(i) + '.txt'
        ans = path + '/ans/' + str(i) + '.txt'
        with open(test, 'w') as file:
            a, b = gen_digit(-100, 100), gen_digit(-100, 100)
            file.write(f"{a} {b}")
        with open(test, 'r') as in_file, open(ans, 'w') as out_file:
            subprocess.run([f'{path}/solution.out'], stdin=in_file, stdout=out_file)


path = 'tasks/contest1/A'

generate()
retest()
