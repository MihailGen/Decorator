from functools import wraps

class Cache:
    def __init__(self):
        self.data = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Проверяем, есть ли результат в кэше,
            # eсли ecть, берем результат из кэш
            if args in self.data:
                result = self.data[args]
                print(f"Результат из КЭШ: {result} для {func.__name__}")

            # Если нет, вызываем функцию и сохраняем результат в кэш
            else:
                result = func(*args, **kwargs)
                self.data[args] = result
                print(f"Новый результат: {result} для {func.__name__}")

            # Возвращаем результат
            return result
            raise NotImplementedError("Заполните эту часть кода")
        return wrapper

    def invalidate(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
        # Инвалидируем кэш для функции
            self.data.clear()
            print(f"Кэш для функцмии {func.__name__} инвалидирован")
            raise NotImplementedError("Заполните эту часть кода")
        return wrapper

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