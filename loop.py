from random import choice

motions = ["motions/head.py", "motions/larm.py", "motions/rarm.py"]

for i in range(4):
    exec(open(choice(motions)).read())