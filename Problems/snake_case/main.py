in_string = input()
new_string = ''
x = in_string[0].lower()
in_string = in_string.replace(in_string[0], x)
for letter in in_string:
    if letter.isupper():
        new_string += ('_' + letter.lower())
    else:
        new_string += letter
print(new_string)
