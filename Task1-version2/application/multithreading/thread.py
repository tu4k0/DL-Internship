import threading

array = []


def fill_array():
    for i in range(1, 10 ** 2):
        array.append(i)
        print(str(len(array)) + ' First thread')
    return array

lock = threading.Lock()

def print_array(thread_num):
    lock.acquire()
    for i in range(len(array)):
        print(str(array[i]) + f' {thread_num}')
    lock.release()


t1 = threading.Thread(target=fill_array, daemon=False)
t2 = threading.Thread(target=print_array, args=('2 thread',), daemon=False)
t3 = threading.Thread(target=print_array, args=('3 thread',), daemon=False)
t4 = threading.Thread(target=print_array, args=('4 thread',), daemon=False)
t5 = threading.Thread(target=print_array, args=('5 thread',), daemon=False)

t1.start()
t1.join()

t2.start()
t3.start()
t4.start()
t5.start()
print(threading.enumerate())

t2.join()
t3.join()
t4.join()
t5.join()