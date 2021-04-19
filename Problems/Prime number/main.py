is_prime = False
number = int(input())
if number >= 2:
    is_prime = True
    for i in range(2, number):
        if number % i == 0:
            is_prime = False
            break
print('This number is prime') if is_prime else print('This number is not prime')