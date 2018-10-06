
from old_jvm1.utils.config import test_state

start = False
def log(*args, **kwargs):
    global start
    if test_state:
        return
    if not start:
        start = True
        open('output', 'w').close()
    print(*args, **kwargs)
    with open('output', 'a+') as f:
        try:
            s = ' '.join(args) + '\n'
        except:
            s = ' '.join(str(args[0])) + '\n'
        f.write(s)
