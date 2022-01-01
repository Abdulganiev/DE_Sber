def is_bigger(num1, num2, eps):
    if round(num1 - num2, 10) >= eps:
        return True
    else:
        return False