from datetime import datetime
import inspect

class Log:
    def __init__(self, name):
        self.name = name
        self.path = f'logs/{datetime.now()} {name}.log'

    def info(self, message):
        stack = inspect.stack()
        message = f'{datetime.now()} [{self.name}] [{stack[1].function}]: {message}'
        print(message)
        self.__write(message)

    def error(self, message):
        stack = inspect.stack()
        message = f'{datetime.now()} [{self.name}] [{stack[1].function}]: ERROR {message}'
        print(message)
        self.__write(message)

    def __write(self, message):
        with open(self.path, 'a') as f:
            f.write(message + '\n')