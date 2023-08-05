from time import perf_counter
import atexit

from performer.formatter import Formatter

class benchmark(object):
    _instance = None
    funcs = []
    loop_counts = []
    logs = []

    def __init__(self, loop_count):
        self.loop_counts.append(loop_count)
        
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            atexit.register(cls.__print_logs)
        
        return cls._instance

    def __call__(self, func): 
        loop_count = self.loop_counts[-1]
        def wrapper(*args, **kwargs):
            start = perf_counter()
            result = func(*args, **kwargs)
            for _ in range(loop_count):
                func(*args, **kwargs)
            total_sec = perf_counter() - start
            if func not in self.funcs:
                self.logs.append([
                    Formatter.func_name(func.__name__),
                    Formatter.return_value(result),
                    Formatter.loop_count(loop_count),
                    Formatter.average(total_sec / loop_count),
                    Formatter.total(total_sec),
                ])
            self.funcs.append(func)
            return result
        
        return wrapper

    @classmethod
    def __print_logs(cls):
        for log in cls.logs:
            print('\n' + '\n'.join(log))
