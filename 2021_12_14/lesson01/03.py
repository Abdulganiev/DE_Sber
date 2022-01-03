n = [int(i) for i in input('укажите ряд чисел через пробел - ').split()]
rez = {}
rez['max'] = max(n)
rez['min'] = min(n)
print(rez)
