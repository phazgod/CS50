def main():
    while True:
        cash = int(input("Change: "))
        if (cash > 0):
            break

    quarters = calculate_quarters(cash)
    cash = cash - (quarters * 25)

    dimes = calculate_dimes(cash)
    cash = cash - (dimes * 10)

    nickels = calculate_nickels(cash)
    cash = cash - (nickels * 5)

    pennies = calculate_pennies(cash)
    cash = cash - (pennies * 1)

    _sum = quarters + dimes + nickels + pennies
    print(f"Total: {_sum}")

def calculate_quarters(n):
    quarters = 0
    while (n >= 25):
        quarters += 1
        n = n - 25
    return quarters

def calculate_dimes(n):
    dimes = 0
    while (n >= 10 and n < 25):
        dimes += 1
        n = n - 10
    return dimes

def calculate_nickels(n):
    nickles = 0
    while (n >= 5 and n < 10):
        nickles += 1
        n = n - 5
    return nickles
def calculate_pennies(n):
    pennies = 0
    while (n < 5 and n > 0):
        pennies += 1
        n = n - 1
    return pennies

main()