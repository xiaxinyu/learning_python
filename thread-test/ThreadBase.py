import threading


def print_time(threadName):
    print(threadName)


t1 = threading.Thread(target=print_time("Thread-1"))
t1.start()
