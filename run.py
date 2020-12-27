import os

flag = True

while flag:
    try:
        result = os.popen('python conceptNet.py')
        res = result.read()
        for line in res.splitlines():
            print(line)
        flag = False
    except:
        flag = True