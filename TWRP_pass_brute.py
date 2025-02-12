#!/bin/python
import itertools
import os

# Параметры
password_symbols = '0123456789'  # Используем только цифры
password_symbols_repeats = True  # Разрешить повторение символов в комбинациях
password_length = 6  # Длина комбинации

# Генерация всех возможных комбинаций
if password_symbols_repeats:
    res = [''.join(x) for x in itertools.product(password_symbols, repeat=password_length)]
else:
    res = [''.join(x) for x in itertools.combinations(password_symbols, password_length)]

combinations_total = len(res)

# Перебор комбинаций
n = 0
for passw in res:
    n += 1
    print("{}/{}: {}".format(n, combinations_total, passw))
    
    # Выполнение команды adb shell twrp decrypt
    cmd_out = os.popen("adb shell twrp decrypt {}".format(passw)).read()
    
    # Проверка результата
    if "Attempting to decrypt data partition via command line" not in cmd_out:
        print(cmd_out)
        print('\nSomething went wrong. Check connection to your device')
        break
    if 'Data successfully decrypted' in cmd_out:
        print("\nYour password is: {}\nBye!".format(passw))
        break
else:
    print("\nNo result.")
