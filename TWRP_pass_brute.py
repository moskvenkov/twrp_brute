#!/usr/bin/env python3
import itertools
import os
import time  # <-- Добавляем модуль для паузы

# Параметры
password_symbols = '0123456789'  # Только цифры
password_symbols_repeats = True  # Разрешить повторения
password_length = 4  # Длина комбинации

# Генерация комбинаций
if password_symbols_repeats:
    res = [''.join(x) for x in itertools.product(password_symbols, repeat=password_length)]
else:
    res = [''.join(x) for x in itertools.combinations(password_symbols, password_length)]

combinations_total = len(res)

n = 0
for passw in res:
    n += 1
    print("{}/{}: {}".format(n, combinations_total, passw))
    
    # Выполняем команду
    cmd_out = os.popen("adb shell twrp decrypt {}".format(passw)).read()
    
    # Проверка на ошибки
    if "Attempting to decrypt data partition via command line" not in cmd_out:
        print(cmd_out)
        print('\nSomething went wrong. Check connection to your device')
        break
    
    # Проверка на успешное декодирование
    if 'Data successfully decrypted' in cmd_out:
        print("\nYour password is: {}\nBye!".format(passw))
        break
    
    time.sleep(0.3)  # <-- Добавляем паузу между попытками

else:
    print("\nNo result.")
