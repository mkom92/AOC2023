from functools import wraps
from time import perf_counter


def timeit(func):
    
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()

        print(f'Total time: {(end_time - start_time):.4f} seconds')
        return result
    return timeit_wrapper