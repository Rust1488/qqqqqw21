def main(a,operator,b):
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '**':
        return a ** b
    elif operator == '/':
        return a / b
    elif operator == '//':
        return a // b
    else:
        return a % b
result = main(float(input("Введите первое число: ")),input("Введите любой из предложенных операторов (+,-,*,**,/,//,%): "),float(input("Введите второе число: ")))
result2 = round(result)
print(result2)