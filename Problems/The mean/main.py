nrs = 0
c = 0
while True:
    i = input()
    if i == '.':
        break
    c += 1
    nrs += int(i)
print(nrs / c)


