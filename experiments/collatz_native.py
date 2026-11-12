"""Глава 7: тот же расчёт последовательностей Коллатца на обычном Python."""
from time import perf_counter

start = perf_counter()
best_n = 0
best_len = 0
total = 0
for n in range(1, 5000):
    x = n
    length = 0
    while x != 1:
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3 * x + 1
        length += 1
    total += length
    if length > best_len:
        best_n = n
        best_len = length

seconds = perf_counter() - start
print('ЛУЧШЕЕ n =', best_n, 'ДЛИНА =', best_len)
print('СУММА ДЛИН =', total)
print('Время обычного Python:', round(seconds, 4), 'с')
