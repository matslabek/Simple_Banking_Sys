number = int(input())
squares = number * number
int_sum = number
while int_sum != 0:
    new_number = int(input())
    int_sum += new_number
    squares += (new_number * new_number)
print(squares)