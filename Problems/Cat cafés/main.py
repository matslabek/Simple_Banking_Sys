word = ''
kitty_cafe = ['None', 1]
while True:
    word = input()
    if word == 'MEOW':
        break
    cafe = word.split()
    if kitty_cafe[1] < int(cafe[1]):
        kitty_cafe[1] = int(cafe[1])
        kitty_cafe[0] = cafe[0]
print(kitty_cafe[0])