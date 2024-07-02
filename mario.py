height = int(input("Height: "))

for i in range(height):
    print(' ' * (height - i - 1), end='')
    print("#" * (i + 1), end ='')
    print(" ", end ='')
    print("#" * (i + 1))