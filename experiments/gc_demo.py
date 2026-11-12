# Глава 6. Эксперимент: сборка мусора в CPython.
import gc
import weakref

class Uzel:
    def __init__(self):
        self.next = None

# Отключаем автоматический поиск циклов.
was_enabled = gc.isenabled()
gc.disable()

# Два узла ссылаются друг на друга.
a = Uzel()
b = Uzel()
a.next = b
b.next = a

# Слабая ссылка позволяет узнать, жив ли объект.
check = weakref.ref(a)
del a
del b

print('До ручной сборки:', 'жив' if check() is not None else 'удалён')
gc.collect()
print('После ручной сборки:', 'жив' if check() is not None else 'удалён')

if was_enabled:
    gc.enable()
