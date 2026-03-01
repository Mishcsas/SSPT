import sys

user_input = sys.stdin.read()
user_input = user_input.lower()
user_input = user_input.split()

if (len(user_input) == 3 and user_input[0].isdigit() and user_input[1].isdigit() and user_input[2].isdigit()):
    res = 1
    for i in range(3):
        res *= int(user_input[i])
    print(res)
else:
    print(0)