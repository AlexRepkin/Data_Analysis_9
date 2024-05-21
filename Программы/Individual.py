#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Lock, Thread


'''Варианты №3 и №2(По списку 28)
С использованием многопоточности для x = 0.7(Во 2) и x = 1.2 (В 3),
находится сумма ряда S с точностью члена ряда по абсолютному
значению ε = 10e^(-7) и производится сравнение полученной суммы с контрольным
значением функции y = 1/(1-x) (Во 2) и y = 1/(2+x) (В 3) для двух бесконечных рядов'''

# Создание блокировки для синхронизации доступа к общему ресурсу (словарю результатов results).
lock = Lock()


def second_var(results):
    # Вычисление суммы ряда для x = 0.7
    s = 0
    n = 0
    while True:
        element = 0.7**n
        if element < 1e-7:  # Проверка условия остановки (ε).
            break
        else:
            s += element
            n += 1
    # Блокировка доступа к общему ресурсу перед записью результата.
    with lock:
        results["second"] = s


def third_var(results):
    # Вычисление суммы ряда для x = 1.2
    s = 0
    n = 0
    while True:
        element = ((-1)**n)*(1.2**n)/2**(n+1)
        if abs(element) < 1e-7:  # Проверка условия остановки (ε).
            break
        else:
            s += element
            n += 1
    # Блокировка доступа к общему ресурсу перед записью результата.
    with lock:
        results["third"] = s


def main():
    results = {}
    # По заданию, y во втором варианте = 1/(1-x). Так как x = 0.7, то y = 10/3
    # y в третьем варианте = 1/(2+x). Так как x = 1.2, то y = 1/(2+1.2) = 0.3125
    y1 = 10/3
    y2 = 0.3125
    # Создание потоков для вычисления сумм.
    first_thread = Thread(target=second_var, args=(results,))
    second_thread = Thread(target=third_var, args=(results,))
    # Запуск созданных потоков.
    first_thread.start()
    second_thread.start()
    # Блокировка основого потока, пока эти два потока не завершатся.
    first_thread.join()
    second_thread.join()

    print("Good day! According to our calculations:\nSum of elements in variant 2 =",
          results["second"])
    print("At the same time, y =", y1, "/n")
    print("For the 3 variant, sum of elements =", results["third"])
    print("y =", y2)


if __name__ == "__main__":
    main()
