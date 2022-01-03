def blunder(n):
    try:
        int(n)
        return True
    except:
        return False

print(blunder('124'))
print(blunder('124f'))