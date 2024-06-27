import asyncio
import hashlib
from functools import wraps

class Cache:
    def __init__(self):
        self.data = {}

    def generate_key(self, func_name, args, kwargs):
        key = f"{func_name}:{args}:{kwargs}"
        return hashlib.md5(key.encode()).hexdigest()

    def __call__(self, func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if func.__name__ not in self.data:
                self.data[func.__name__] = {}

            # делаем ключ из аргументов
            key = str(args) + str(kwargs)

            # Проверяем, есть ли результат в кэше,
            # eсли ecть, берем результат из кэш
            if key in self.data[func.__name__]:
                return self.data[func.__name__][key]

            # поскольку функция асинхронная, ответ надо подождать
            ans = await func(*args, *kwargs)
            self.data[func.__name__][key] = ans
            return ans

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            if func.__name__ not in self.data:
                self.data[func.__name__] = {}

            key = str(args) + str(kwargs)
            # Проверяем, есть ли результат в кэше,
            # eсли ecть, берем результат из кэш
            if key in self.data[func.__name__]:
                return self.data[func.__name__][key]

            # Если нет, вызываем функцию и сохраняем результат в кэш
            ans = func(*args, *kwargs)
            self.data[func.__name__][key] = ans
            return ans

        # Распознаём,асинхронная функция, или нет и в зависимости от этого выбираем враппер
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper


    def invalidate(self, func):
        if func.__name__ in self.data:
            del self.data[func.name]

cache = Cache()

@cache
def slow_function(arg):
    return arg

class MyClass:
    @cache
    def method(self, arg):
        return arg

@cache
async def async_func(arg):
    return arg

p = MyClass()
p.method(4)
p.method(4)