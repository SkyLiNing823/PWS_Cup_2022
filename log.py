import os
f = open("log.txt")
line = f.readline()
while line:
    print(line)
    os.system('python '+line)
    line = f.readline()
f.close()
