import random

motions = ["motions/head.py", "motions/larm.py", "motions/rarm.py"]

for i in range(4):
    exec(open(random.choice(motions)).read())