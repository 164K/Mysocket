import threading
import typing
import time

def simple_func(x: int):
    print("Start")
    time.sleep(1)
    return x

th = threading.Thread(target=simple_func, args=(1,))
th.start()
time.sleep(2)
print(th.is_alive())
