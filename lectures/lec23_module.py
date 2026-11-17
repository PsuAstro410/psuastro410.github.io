import numpy as np
import os
import multiprocessing as mp

def doubler(number):
    """
    A doubling function that can be used by a process
    """
    result = number * 2
    proc = os.getpid()
    print('{0} doubled to {1} by process id: {2}'.format(number, result, proc))
    return result

def doubler_troubler(number):
    """
    A doubling function that can be used by a process
    also displays current process
    """
    result = number * 2
    proc_name = mp.current_process().name
    print('{0} doubled to {1} by: {2}'.format(
        number, result, proc_name))

def doubler_simple(number):
    return number * 2

def creator(data, q):
    """
    Creates data to be consumed and waits for the consumer
    to finish processing
    """
    print('Creating data and putting it on the queue')
    for item in data:
        
        q.put(item)

sentinel = -1
        
def my_consumer(q):
    """
    Consumes some data and works on it
    In this case, all it does is double the input
    """
    while True:
        data = q.get()
        print('data found to be processed: {}'.format(data))
        processed = data * 2
        print(processed)
        
        if data is sentinel:
            break

def random_square(seed):
    np.random.seed(seed)
    random_num = np.random.randint(0, 10)
    return random_num**2

def plus_cube(x, y):
    return (x+y)**3