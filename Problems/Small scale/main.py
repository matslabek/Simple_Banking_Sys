numbers = []
while True:
    numb = input()
    if numb != '.':
        numbers.append(float(numb))
    else:
        break
print(min(numbers))