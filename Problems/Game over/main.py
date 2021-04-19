scores = input().split()
lives = 3
points = 0
for ans in scores:
    if 'C' == ans:
        points += 1
    if 'I' == ans:
        lives -= 1
        if lives == 0:
            print('Game over\n' + str(points))
            break
else:
    print('You won\n' + str(points))